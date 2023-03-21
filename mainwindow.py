import ctypes
import sys
import adb
from PyQt6.QtGui import QIcon, QTextCursor
from PyQt6.QtCore import QSize, QObject, pyqtSignal, Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QPlainTextEdit, QVBoxLayout, QWidget, \
    QLabel, QGridLayout, QComboBox, QMessageBox
from emulatorwindow import EmulatorWindow
from threadmanager import ThreadManager
from emulator import Emulator
from ldconsole import Ldconsole


class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        sys.stdout = Stream(newText=self.onUpdateText)
        self.setWindowTitle("Autoreg")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(QSize(640, 480))

        self.thread_manager = ThreadManager()

        self.emulator_window = EmulatorWindow(self, Qt.WindowType.Widget)
        self.emulator_window.setVisible(True)
        # self.browser_window = BrowserWindow(self, Qt.WindowType.Widget)

        # Main Grid and Widgets
        self.registration_type_text = QLabel("Registration Type:")
        self.registration_type = QComboBox()
        self.registration_type.addItems(["Facebook (LDPlayer)"])
        self.registration_type.currentIndexChanged.connect(self.changeState)
        main_grid = QGridLayout()
        main_grid.setSpacing(10)
        main_grid.addWidget(self.registration_type_text, 0, 0)
        main_grid.addWidget(self.registration_type, 0, 1, Qt.AlignmentFlag.AlignLeading, 6)

        self.logger = QPlainTextEdit()
        self.logger.setReadOnly(True)

        self.button = QPushButton("Start")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.btnstate)

        main_layout = QVBoxLayout()
        main_layout.addLayout(main_grid)
        # main_layout.addWidget(self.browser_window)
        main_layout.addWidget(self.emulator_window)
        main_layout.addWidget(self.logger)
        main_layout.addWidget(self.button)

        # # Устанавливаем центральный виджет Window.
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def changeState(self):
        if self.registration_type.currentIndex() == 0:
            self.emulator_window.show()
            # self.browser_window.show()

    def onUpdateText(self, text):
        cursor = self.logger.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.logger.setTextCursor(cursor)
        self.logger.ensureCursorVisible()

    def thread_complete(self):
        print("Complete!")
        self.thread_manager.set_thread_running(False)
        self.button.setEnabled(True)

    def connected(self):
        self.button.setEnabled(True)

    def btnstate(self):
        if self.button.isEnabled():
            self.button.setEnabled(False)
            if self.registration_type.currentIndex() == 0:
                emulator = Emulator()
                emulator.signals.connected.connect(self.connected)
                self.emulator_window.run_thread(emulator)
        else:
            self.button.setEnabled(True)

    def closeEvent(self, event):
        if self.thread_manager.activeThreadCount() == 0:
            reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                sys.stdout = sys.__stdout__  # restore stdout before quitting
                event.accept()
                if adb.AdbManager.all_indices:
                    ld_console = Ldconsole()
                    ld_console.set_path(ld_console.get_spath())
                    # print(ld_console.get_path())
                    for i in adb.AdbManager.all_indices:
                        ld_console.remove_by_index(i)
            else:
                event.ignore()
        else:
            reply = QMessageBox.warning(self, 'Warning', 'You cannot close the program because the program is already running. Wait until the end of the program execution.')
            if reply == QMessageBox.StandardButton.Ok:
                event.ignore()
            else:
                event.ignore()
