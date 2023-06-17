import logging
import typing as t

from pydantic import BaseModel
from zope.interface import Interface
from apscheduler.jobstores.base import JobLookupError

from .biz_exception import BIZException
from internal.modules import redisx
from internal.modules import schedulerx


class TokenStatus:
    STARTED = 1
    NOT_START = 0


class CreateTokenReq(BaseModel):
    topic: str
    bucket: int
    token_per_second: int


class GetTokenReq(BaseModel):
    topic: str
    count: int


class Token(BaseModel):
    id: int = 0
    topic: str
    bucket: int
    token_per_second: int
    status: int = 1


class ITokenSystemRepo(Interface):
    """"""
    def get_started_tokens(self) -> t.List[Token]:
        """获取所有启动的token"""

    def is_exist_topic(self, topic: str) -> bool:
        """topic是否已经存在"""

    def get_token_by_topic(self, topic) -> t.Optional[Token]:
        """通过topic获取token"""

    def create_token(self, req: CreateTokenReq):
        """create token interface"""

    def is_already_start_by_topic(self, topic: str):
        """判断是否已经启动"""

    def update_token_status_by_id(self, tid: int, status: int):
        """更新token的状态"""

    def get_token(self):
        """get token interface"""

    def delete_token(self, topic: str):
        """delete token interface"""


class TokenSystemUseCase:
    """"""

    __slots__ = ('_repo', )

    def __init__(self, repo: ITokenSystemRepo):
        self._repo = repo
        self._init_token()

    def _init_token(self):
        """初始化token, 数据库中状态为1的全部拉起"""
        tokens = self._repo.get_started_tokens()
        for token in tokens:
            self._start_token(token)

    def create_token(self, req: CreateTokenReq):
        if not req.topic:
            raise BIZException.ErrTopicIsNull

        if len(req.topic) < 6:
            raise BIZException.ErrTopicNotExactly

        if req.bucket <= 0:
            raise BIZException.ErrBucketNotExactly

        if req.token_per_second <= 0:
            raise BIZException.ErrTokenPerSecondNotExactly

        if self._repo.is_exist_topic(req.topic):
            raise BIZException.ErrTopicAlreadyExist

        return self._repo.create_token(req)

    def start_token(self, topic: str):
        if not topic:
            raise BIZException.ErrTopicIsNull

        if len(topic) < 6:
            raise BIZException.ErrTopicNotExactly

        token = self._repo.get_token_by_topic(topic)
        if token is None:
            raise BIZException.ErrTokenNotExist

        if token.status == TokenStatus.STARTED:
            raise BIZException.ErrTokenAlreadyStart

        self._start_token(token)

        self._repo.update_token_status_by_id(token.id, TokenStatus.STARTED)

    @staticmethod
    def _start_token(token: Token):
        token_key = f'token-system:{token.topic}'
        token_bucket = f'token-system:{token.topic}:bucket:{token.bucket}'

        # 在redis中设置token信息
        redisx.redis.cli.set(token_key, 0)
        redisx.redis.cli.set(token_bucket, token.bucket)

        timer = 1 / token.token_per_second

        def _start_token_job(_topic_key: str, _bucket_key: str):
            if not redisx.redis.cli.exists(_topic_key):
                redisx.redis.cli.set(_topic_key, 0)
                redisx.redis.cli.set(_bucket_key, token.bucket)

            if int(redisx.redis.cli.get(_topic_key)) < int(redisx.redis.cli.get(_bucket_key)):
                redisx.redis.cli.incr(_topic_key)

        schedulerx.cli.add_job(
            _start_token_job,
            'interval',
            seconds=timer,
            args=(token_key, token_bucket),
            id=token_key
        )

    def get_token(self, req: GetTokenReq):
        if not req.topic:
            raise BIZException.ErrTopicIsNull

        if len(req.topic) < 6:
            raise BIZException.ErrTopicNotExactly

        token = self._repo.get_token_by_topic(req.topic)
        if token is None:
            raise BIZException.ErrTokenNotExist

        if token.status == TokenStatus.NOT_START:
            raise BIZException.ErrTokenNotStart

        if req.count > token.bucket:
            raise BIZException.ErrOutOfRangeBucket

        token_key = f'token-system:{req.topic}'

        if int(redisx.redis.cli.get(token_key)) < req.count:
            raise BIZException.ErrNotEnoughToken

        # 申请令牌
        redisx.redis.cli.decr(token_key, req.count)

    def delete_token(self, topic: str):
        if not topic:
            raise BIZException.ErrTopicIsNull

        if len(topic) < 6:
            raise BIZException.ErrTopicNotExactly

        token_key = f'token-system:{topic}'

        # 1. 删除scheduler任务
        try:
            schedulerx.cli.remove_job(job_id=token_key)
        except JobLookupError:
            logging.info(f'{token_key} job not exist')

        # 2. 删除redis中的数据
        redisx.redis.cli.delete(*redisx.redis.cli.keys(f'{token_key}*'))

        # 3. 删除数据库任务
        self._repo.delete_token(topic)


def new_token_system_use_case(repo: ITokenSystemRepo) -> TokenSystemUseCase:
    return TokenSystemUseCase(repo)
