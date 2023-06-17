import os
import logging
import logging.handlers
import pathlib
from enum import Enum, unique

from internal.modules.utils import Singleton


@unique
class LoggerRotatingType(Enum):
    SIZE = 1
    TIMED = 2


class Logger(Singleton):
    """logger format"""
    def __init__(
            self,
            log_path: str,
            name: str,
            level: str = 'info',
            fmt: str = None,
            back_count: int = 10,
            encoding: str = 'utf-8',
            typ: LoggerRotatingType = LoggerRotatingType.SIZE,
            when: str = 'D',
            max_bytes: int = 20 * 1024 * 1024,
    ):
        """
        初始化
        :param log_path: log 路径
        :param name: log日志名
        :param level: 等级
        :param fmt: 格式
        :param back_count: 备份个数
        :param encoding: 编码
        :param typ: 滚动格式, 根据大小滚动和时间滚动两种模式
        :param when: 在根据时间滚动是设置, 默认是天 'D'
        :param max_bytes: 超过多少的时候创建新的日志文件, 大小滚动时设置
        """
        self._log_path = log_path
        self._name = name
        self._level = level
        self._fmt = fmt if fmt \
            else logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        self._back_count = back_count
        self._typ = typ
        self._when = when
        self._encoding = encoding
        self._max_size = max_bytes

    def init(self):
        # 1. level, 默认 info级别
        level_name = os.environ.get('DEFAULT_LOG_LEVEL', self._level)
        level = logging.getLevelName(level_name)
        if not isinstance(level, int):
            level = logging.INFO

        # 2. base logger, 默认终端输出
        logging.basicConfig(
            level=level,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filemode='w')

        # 3. 设置日志文件输入
        if not os.path.isdir(self._log_path):
            os.makedirs(self._log_path)

        # log file
        log_file = pathlib.Path(os.path.join(self._log_path, self._name)).as_posix()

        if self._typ == LoggerRotatingType.SIZE:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=self._max_size,
                backupCount=self._back_count,
                encoding=self._encoding
            )
        else:
            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=log_file,
                when=self._when,
                backupCount=self._back_count,
                encoding=self._encoding
            )
        file_handler.setFormatter(self._fmt)
        logging.getLogger().addHandler(file_handler)
