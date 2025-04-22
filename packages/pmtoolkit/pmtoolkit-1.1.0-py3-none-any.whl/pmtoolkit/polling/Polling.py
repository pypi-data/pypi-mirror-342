import functools
import sys
import time


class Polling:
    """_轮询重试装饰器_
    """
    def __init__(self, timeout=10, polling_interval=0.5):
        """_初始化_

        Args:
            timeout (int, optional): _超时时间（s）_. Defaults to 10.
            polling_interval (float, optional): _轮询间隔时间（s）_. Defaults to 0.5.
        """
        self.timeout = timeout
        self.polling_interval = polling_interval

    def polling_handler(self, func):
        """_将某个校验函数变为轮询检查函数的装饰器_

        Args:
            func (_type_): _需要检查的条件函数_
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            while time.time() - start_time < self.timeout:
                if func(*args, **kwargs):
                    return True
                time.sleep(self.polling_interval)
            return False

        return wrapper

    @staticmethod
    def polling_with_condition(condition_func, timeout=10, polling_interval=0.5):
        """_内部静态方法，用于传入一个函数作为轮询检查函数_

        Args:
            condition_func (_type_): _检查函数_
            timeout (int, optional): _超时时间（s）_. Defaults to 10.
            polling_interval (float, optional): _轮询间隔时间（s）_. Defaults to 0.5.

        Returns:
            _type_: _description_
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(polling_interval)
        return False

    # 示例轮询查找UI控件函数，后期视需求扩充
    @staticmethod
    def polling_pane_exists(class_name):
        """_轮询检查某个window或pane是否存在_

        Args:
            class_name (_type_): _窗口类名_

        Raises:
            Exception: _只支持windows系统，其他系统使用该方法抛出异常_
        """
        if sys.platform.startswith('win'):
            import uiautomation as auto

            def win_func():
                if auto.PaneControl(ClassName=class_name).Exists():
                    return True
                elif auto.WindowControl(ClassName=class_name).Exists():
                    return True
                else:
                    return False

            return Polling.polling_with_condition(win_func())
        else:
            raise Exception('未知操作系统')

    @staticmethod
    def polling_controller_exists(pane, controller_id):
        """_轮询检查某个控件是否存在_

        Args:
            pane (_type_): _控件所在pane_
            controller_id (_type_): _要寻找的控件id_


         Raises:
            Exception: _只支持windows系统，其他系统使用该方法抛出异常_
        """
        if sys.platform.startswith('win'):

            def win_func():
                if pane.Control(AutomationId=str(id)).Exists(controller_id):
                    return True
                else:
                    return False

            return Polling.polling_with_condition(win_func())
        else:
            raise Exception('未知操作系统')
