import sys

# 全局捕获异常类


class GlobalException(Exception):
    def __init__(self, logger):
        """初始化

        Args:
            logger (_type_): 传入一个日志处理器
        """
        self.logger = logger

    # 处理全局异常
    def handle_exception(self, exception_type, value, traceback):
        """处理全局异常

        Args:
            exception_type (_type_): 异常类型
            value (_type_): 异常信息
            traceback (_type_): traceback位置
        """
        print(traceback)
        self.logger.error(value)

    # 注册全局异常捕获器
    def register(self):
        sys.excepthook = self.handle_exception
