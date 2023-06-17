class BIZException:
    """biz level exception"""

    class ErrInternalServer(Exception):
        """服务内部错误异常"""

    class ErrTopicNotExist(Exception):
        """topic不存在异常"""

    class ErrTopicIsNull(Exception):
        """topic为空"""

    class ErrTopicNotExactly(Exception):
        """topic格式不正确"""

    class ErrTopicAlreadyExist(Exception):
        """topic已经存在"""

    class ErrTokenNotExist(Exception):
        """token不存在"""

    class ErrTokenAlreadyStart(Exception):
        """该token已经启动"""

    class ErrTokenNotStart(Exception):
        """token没有启动"""

    class ErrOutOfRangeBucket(Exception):
        """超出桶的最大容量"""

    class ErrNotEnoughToken(Exception):
        """没有足够的令牌"""

    class ErrBucketNotExactly(Exception):
        """bucket size 不能小于等于0"""

    class ErrTokenPerSecondNotExactly(Exception):
        """token per second 不能小于等于0"""

    class ErrStartTokenFailed(Exception):
        """启动token失败"""
