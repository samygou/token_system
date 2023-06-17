import time
import typing as t
import logging

from zope.interface import implementer

from internal import biz
from . import orm


@implementer(biz.ITokenSystemRepo)
class TokenSystemRepo:
    """"""
    def __init__(self):
        """"""

    def get_started_tokens(self) -> t.List[biz.Token]:
        sql = f"""SELECT id, topic, bucket, token_per_second FROM token_system WHERE status = 1"""

        with orm.DBSession(orm.db) as sess:
            results = sess.execute_all(sql)

        if results:
            results = list(map(lambda result: biz.Token(**result), results))

        return results

    def is_exist_topic(self, topic: str) -> bool:
        """topic是否已存在"""
        sql = f"""SELECT id FROM token_system WHERE topic = '{topic}'"""

        with orm.DBSession(orm.db) as sess:
            result = sess.execute(sql)
            if not result:
                return False

        return True

    def create_token(self, req: biz.CreateTokenReq):
        """"""
        try:
            timestamp = int(time.time())
            sql = f"""INSERT INTO token_system(topic, bucket, token_per_second, create_time, update_time) VALUES(
            '{req.topic}', {req.bucket}, {req.token_per_second}, {timestamp}, {timestamp})"""
            logging.info(sql)
            with orm.DBSession(orm.db) as sess:
                result = sess.execute(sql)
            logging.info(req)
        except orm.DBException.InternalErr:
            raise biz.BIZException.ErrInternalServer
        except Exception as e:
            logging.error(e)
            raise biz.BIZException.ErrInternalServer

    def get_token_by_topic(self, topic: str) -> t.Optional[biz.Token]:
        sql = f"""SELECT id, topic, bucket, token_per_second, status FROM token_system WHERE topic = '{topic}'"""

        try:
            with orm.DBSession(orm.db) as sess:
                result = sess.execute_all(sql)
                if not result:
                    return None
                return biz.Token(**result[0])
        except orm.DBException.InternalErr:
            raise biz.BIZException.ErrInternalServer
        except Exception as e:
            logging.error(e)
            raise biz.BIZException.ErrInternalServer

    def update_token_status_by_id(self, tid: int, status: int):
        sql = f"""UPDATE token_system SET status = {status} WHERE id = {tid}"""

        try:
            with orm.DBSession(orm.db) as sess:
                sess.execute(sql)
        except orm.DBException.InternalErr:
            raise biz.BIZException.ErrInternalServer
        except Exception as e:
            logging.error(e)
            raise biz.BIZException.ErrInternalServer

    def delete_token(self, topic: str):
        sql = f"""DELETE FROM token_system WHERE topic = '{topic}'"""

        try:
            with orm.DBSession(orm.db) as sess:
                sess.execute(sql)
        except Exception as e:
            logging.error(e)
            raise biz.BIZException.ErrInternalServer


def new_token_system_repo() -> TokenSystemRepo:
    return TokenSystemRepo()
