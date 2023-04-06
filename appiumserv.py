import os
import time
import psutil
# from appium.webdriver.appium_service import AppiumService


class AppiumServer:
    '''
    Статический объект класса AppiumService.
    '''

    # appium_service = AppiumService()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AppiumServer, cls).__new__(cls)
        return cls.instance

    # @staticmethod
    # def start():
    #     AppiumServer.appium_service.start(timeout_ms=999000)
    #
    # @staticmethod
    # def is_running():
    #     if AppiumServer.appium_service.is_running:
    #         return True
    #     else:
    #         return False
    #
    # @staticmethod
    # def stop():
    #     AppiumServer.appium_service.stop()

    @staticmethod
    def start(address='127.0.0.1', port='4723', timeout='999000'):
        os.system(
            "start /B start cmd.exe @cmd /c appium -a " + address + " -p " + port + " --command-timeout " + timeout)

    @staticmethod
    def is_running():
        '''
        Проверяет запущен ли сервер Appium (Node).
        Если сервер запущен, то возвращает True, если нет - False.
        '''
        # Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if 'Node'.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    @staticmethod
    def forced_stop():
        while True:
            procname = "node.exe"
            # procname2 = "cmd.exe"
            for proc in psutil.process_iter():
                # check whether the process name matches
                # if proc.name() == procname or proc.name() == procname2:
                if proc.name() == procname:
                    proc.kill()
                    return
            time.sleep(1)

    @staticmethod
    def stop():
        procname = "node.exe"
        # procname2 = "cmd.exe"
        for proc in psutil.process_iter():
            # check whether the process name matches
            # if proc.name() == procname or proc.name() == procname2:
            if proc.name() == procname:
                proc.kill()
