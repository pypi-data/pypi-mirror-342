import contextlib
import functools
import logging
import os
import sys
from logging.config import dictConfig
from typing import Literal


# 日志类
class Logger:
    def __init__(self, logger_level: Literal['INFO', 'DEBUG', 'ERROR', 'CRITICAL', 'WARNING'], logger_name: str = ""):
        """初始化

        Args: logger_level (Literal['INFO', 'DEBUG', 'ERROR', 'CRITICAL', 'WARNING']) : 定义日志处理器级别['INFO', 'DEBUG',
        'ERROR', 'CRITICAL', 'WARNING'] logger_name (str, optional): 日志处理器名称. 默认 "".
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logger_level)

    # 创建stdout/stderr处理器
    def add_stream_handler(self, handler_type: Literal['stdout', 'stderr'],
                           handler_level: Literal['INFO', 'DEBUG', 'ERROR', 'CRITICAL', 'WARNING'],
                           handler_formatter: str = "") -> logging.Handler:
        """创建一个stderr/stdout处理器

        Args:
            handler_type (Literal['stdout', 'stderr']): 声明一个stderr或stdout处理器
            handler_level (Literal['INFO', 'DEBUG', 'ERROR', 'CRITICAL', 'WARNING']): 处理器级别，传入后该级别以下的日志信息不会捕获
            handler_formatter (str, optional): 处理器输出日志格式. 默认为%(asctime)s - %(levelname)s - %(message)s，可展示信息参考：
                                                %(asctime)s：‌显示日志记录的时间，‌格式为%Y-%m-%d %H:%M:%S。‌
                                                %(name)s：‌显示日志记录的名称。‌
                                                %(levelname)s：‌显示日志记录的级别。‌
                                                %(message)s：‌显示日志记录的消息。‌
                                                %(filename)s：‌显示产生日志的源文件名。‌
                                                %(lineno)d：‌显示产生日志的源代码行号。‌
        Raises:
            ValueError: 只能传入stdout/stderr类型，其他类型抛出异常

        Returns:
            logging.Handler: 返回创建的日志处理器
        """

        # 格式化
        if handler_formatter == "":
            handler_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        else:
            handler_formatter = logging.Formatter(handler_formatter)

        # 设置类型
        if handler_type == "stdout":
            handler = logging.StreamHandler(sys.stdout)
        elif handler_type == "stderr":
            handler = logging.StreamHandler(sys.stderr)
        else:
            raise ValueError("Invalid handler type")

        # 设置级别
        handler.setLevel(handler_level)

        # 格式化
        handler.setFormatter(handler_formatter)

        # 添加处理器
        self.logger.addHandler(handler)

        return handler

    # 创建file处理器，将日志输出到指定文件路径中
    def add_file_handler(self, file_path: str, file_mode: str = "a",
                         handler_level: Literal['INFO', 'DEBUG', 'ERROR', 'CRITICAL', 'WARNING'] = "DEBUG",
                         file_encoding: str = "UTF-8", delay: bool = False,
                         handler_formatter: str = "") -> logging.Handler:

        """创建file处理器，将日志输出到指定文件路径中

        Args:
            file_path (str): 输出文件路径（包含文件名）
            file_mode (str, optional): 文件读取方式（'r','w','a'等）. 默认 "a".
            handler_level ((Literal['INFO', 'DEBUG', 'ERROR', 'CRITICAL', 'WARNING']), optional): 处理器级别，传入后该级别以下的日志信息不会捕获. 默认为 "DEBUG".
            file_encoding (str, optional): 文件编码方式. 默认 "UTF-8".
            delay (bool, optional): 是否延迟写入文件，不建议开启. 默认 False.
            handler_formatter (str, optional): 处理器输出日志格式，详情参考add_stream_handler中的handler_formatter参数.

        Returns:
            logging.Handler: 返回创建的日志处理器
        """
        # 没有文件的话创建文件
        if not os.path.exists(file_path):
            open(file_path, "w")

        file_handler = logging.FileHandler(file_path, file_mode, file_encoding, delay)

        # 设置级别
        file_handler.setLevel(handler_level)

        # 格式化
        if handler_formatter == "":
            handler_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        else:
            handler_formatter = logging.Formatter(handler_formatter)
        file_handler.setFormatter(handler_formatter)

        # 加入logger中
        self.logger.addHandler(file_handler)
        return file_handler

    # 移除处理器
    def remove_handler(self, handler: logging.Handler) -> None:
        """移除某个处理器

        Args:
            handler (logging.Handler): 传入创建的处理器
        """
        self.logger.removeHandler(handler)

    # 控制台输出日志信息
    def info(self, message: str):
        """输出info级别日志

        Args:
            message (str): 日志信息
        """
        self.logger.info(message)

    def debug(self, message: str):
        """输出debug级别日志

        Args:
            message (str): 同info函数
        """
        self.logger.debug(message)

    def error(self, message: str):
        """输出error级别日志

        Args:
            message (str): 同info函数
        """
        self.logger.error(message)

    def critical(self, message: str):
        """输出critical级别日志

        Args:
            message (str): 同info函数
        """
        self.logger.critical(message)

    def warning(self, message: str):
        """输出waring级别日志

        Args:
            message (str): 同info函数
        """
        self.logger.warning(message)

    # 创建函数打印装饰器
    """
        打印整个函数中的日志以及返回值
        @logger.logging_function
        def test_function():
            return 1
    """

    @staticmethod
    def logging_function(logger):
        """创建装饰器形式的日志收集器，以装饰器形式调用后获取被装饰整个函数中的日志信息

        Args:
            func (_type_): 被装饰函数
            logger(_type_): 需要哪个logger装饰函数

        Returns:
            _type_: 返回装饰器函数
        """

        def decorator(func):

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    logger.info(f"调用函数名: {func.__name__};参数：{args};关键字参数：{kwargs}")
                    result = func(*args, **kwargs)
                    logger.info(f"函数{func.__name__}的结果为：{result}")
                    return result
                except Exception as e:
                    logger.error(f"函数{func.__name__}抛出异常：{e}")

            return wrapper

        return decorator

    # 收集上下文中所有的日志并输出
    """
        打印整个上下文中日志并输出（迭代器）
        with logger.logging_context(test_function):
            ......
            pass
    """

    @staticmethod
    @contextlib.contextmanager
    def logging_context(logger, message):
        """收集上下文中的所有日志并输出

        Args:
            message (_type_): 上下文名称
            logger:需要哪个logger执行
        """
        logger.info(f"进入上下文：{message}")
        try:
            yield
        except Exception as e:
            logger.error(f"上下文{message}中出现异常：{e}")
        finally:
            logger.info(f"退出上下文：{message}")

    # 读取字典配置创建日志
    @staticmethod
    def dict_config(config):
        """根据.yaml或.json配置文件生成日志处理器

               Args:
                   config (_type_): 配置文件

               """
        dictConfig(config)

    @staticmethod
    def get_logger(logger_name: str):
        return logging.getLogger(logger_name)
    # def set_interval_remover(self, interval:int,path:str)->None
