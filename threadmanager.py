from PyQt6.QtCore import QThreadPool


class ThreadManager(QThreadPool):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ThreadManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.is_thread_running = False

    def set_thread_running(self, boolean):
        self.is_thread_running = boolean

    def get_thread_running(self):
        return self.is_thread_running
