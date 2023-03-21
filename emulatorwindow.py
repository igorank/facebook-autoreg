# import sys
# from random import randint
# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QLabel, QVBoxLayout, QWidget, QLineEdit, QGridLayout,
                             QComboBox, QSpinBox, QCheckBox)
# from emulator import Emulator
from threadmanager import ThreadManager
from appiumserv import AppiumServer


class EmulatorWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window.
    """
    def __init__(self, parent=None, flags=None):
        super().__init__(parent, flags)

        #self.emulator = Emulator()
        self.thread_manager = ThreadManager()

        self.ldplayer_path_text = QLabel("Path to LDPlayer:")
        self.ldpayer_geo_text = QLabel("Geolocation:")
        ldpayer_geo_list = ["UA", "SK", "RU", "GB", "PL", "KZ", "EE"]
        ldpayer_geo_list.sort()
        self.ldpayer_geo = QComboBox()
        self.ldpayer_geo.addItems(ldpayer_geo_list)
        self.loop_numbers_text = QLabel("Loop Request:")
        self.loop_numbers = QCheckBox()
        self.sms_activate_api_key_text = QLabel("SMS Activate API Token:")
        self.country_number_text = QLabel("Country:")
        self.ldplayer_path = QLineEdit()
        self.sms_activate_api_key = QLineEdit()
        self.country_number = QComboBox()
        country_number_list = ["RU", "UA", 'KZ', 'PH', 'ID', 'MY', 'VN', 'KG', 'PL', 'GB', 'IN', 'SK', "EE"]
        country_number_list.sort()
        self.country_number.addItems(country_number_list)
        self.emails_list_text = QLabel("List of Emails:")
        self.emails_list = QLineEdit()
        self.emails_list.setEnabled(False)
        self.use_eamil_text = QLabel("Use Email Addresses:")
        self.use_eamil = QCheckBox()
        self.use_proxy_text = QLabel("Use Proxy:")
        self.use_proxy = QCheckBox()
        self.use_proxy.setChecked(True)
        self.delete_dalvik_cache_text = QLabel("Delete dalvik-cache:")
        self.delete_dalvik_cache = QCheckBox()
        self.delete_dalvik_cache.setChecked(False)

        self.use_eamil.stateChanged.connect(self.use_email_changed)
        self.use_proxy.stateChanged.connect(self.use_proxy_changed)

        self.proxy_type_text = QLabel("Proxy Type:")
        self.proxy_host_text = QLabel("Proxy Host:")
        self.proxy_port_text = QLabel("Proxy Port:")
        self.proxy_login_text = QLabel("Proxy Login:")
        self.proxy_password_text = QLabel("Proxy Password:")
        self.num_of_profiles_text = QLabel("Iterations:")
        self.change_ip_url_text = QLabel("Change IP URL:")

        self.proxy_type = QComboBox()
        self.proxy_type.addItems(["socks5"])
        self.proxy_host = QLineEdit()
        self.proxy_port = QLineEdit()
        self.proxy_login = QLineEdit()
        self.proxy_password = QLineEdit()
        self.num_of_profiles = QSpinBox()
        self.num_of_profiles.setMinimum(1)
        self.num_of_profiles.setMaximum(9999999)
        self.change_ip_url = QLineEdit()

        # DEBUG
        self.ldplayer_path.setText(r"C:\LDPlayer\LDPlayer4.0")
        self.emails_list.setText(r"C:\Users\Igor\Documents\Projects\Facebook-autoreg\emails.txt")
        self.proxy_host.setText("oproxy.site")
        self.proxy_port.setText("12536")
        self.proxy_login.setText("SUV4FU")
        self.proxy_password.setText("eT3PAwKEqavC")
        self.change_ip_url.setText("https://mobileproxy.space/reload.html?proxy_key=d7b59504de76caa1d494e882584cca74")

        api_grid = QGridLayout()
        api_grid.setSpacing(10)
        api_grid.addWidget(self.ldplayer_path_text, 1, 0)
        api_grid.addWidget(self.ldplayer_path, 1, 1)
        api_grid.addWidget(self.ldpayer_geo_text, 1, 2)
        api_grid.addWidget(self.ldpayer_geo, 1, 3)
        api_grid.addWidget(self.sms_activate_api_key_text, 2, 0)
        api_grid.addWidget(self.sms_activate_api_key, 2, 1)
        api_grid.addWidget(self.country_number_text, 2, 2)
        api_grid.addWidget(self.country_number, 2, 3)
        api_grid.addWidget(self.emails_list_text, 3, 0)
        api_grid.addWidget(self.emails_list, 3, 1)
        api_grid.addWidget(self.use_eamil_text, 3, 2)
        api_grid.addWidget(self.use_eamil, 3, 3)

        proxy_grid = QGridLayout()
        proxy_grid.setSpacing(10)
        proxy_grid.addWidget(self.use_proxy_text, 3, 0)
        proxy_grid.addWidget(self.use_proxy, 3, 1)
        proxy_grid.addWidget(self.proxy_type_text, 4, 0)
        proxy_grid.addWidget(self.proxy_type, 4, 1)
        proxy_grid.addWidget(self.proxy_host_text, 3, 2)
        proxy_grid.addWidget(self.proxy_host, 3, 3)
        proxy_grid.addWidget(self.proxy_port_text, 3, 4)
        proxy_grid.addWidget(self.proxy_port, 3, 5)
        proxy_grid.addWidget(self.proxy_login_text, 4, 2)
        proxy_grid.addWidget(self.proxy_login, 4, 3)
        proxy_grid.addWidget(self.proxy_password_text, 4, 4)
        proxy_grid.addWidget(self.proxy_password, 4, 5)
        proxy_grid.addWidget(self.num_of_profiles_text, 3, 6)
        proxy_grid.addWidget(self.num_of_profiles, 3, 7)
        proxy_grid.addWidget(self.loop_numbers_text, 4, 6)
        proxy_grid.addWidget(self.loop_numbers, 4, 7)

        change_ip_grid = QGridLayout()
        change_ip_grid.setSpacing(10)
        change_ip_grid.addWidget(self.change_ip_url_text, 0, 0)
        change_ip_grid.addWidget(self.change_ip_url, 0, 1)
        change_ip_grid.addWidget(self.delete_dalvik_cache_text, 0, 2)
        change_ip_grid.addWidget(self.delete_dalvik_cache, 0, 3)
        # change_ip_grid.addWidget(self.loop_numbers_text, 0, 2)
        # change_ip_grid.addWidget(self.loop_numbers, 0, 3)

        layout = QVBoxLayout()
        layout.addLayout(api_grid)
        layout.addLayout(proxy_grid)
        layout.addLayout(change_ip_grid)
        self.setLayout(layout)

    def use_email_changed(self):
        if self.use_eamil.isChecked():
            self.emails_list.setEnabled(True)
            self.sms_activate_api_key.setEnabled(False)
            self.loop_numbers.setEnabled(False)
            self.country_number.setEnabled(False)
            self.num_of_profiles.setEnabled(False)
        else:
            self.emails_list.setEnabled(False)
            self.sms_activate_api_key.setEnabled(True)
            self.loop_numbers.setEnabled(True)
            self.country_number.setEnabled(True)
            self.num_of_profiles.setEnabled(True)

    def use_proxy_changed(self):
        if self.use_proxy.isChecked():
            self.proxy_type.setEnabled(True)
            self.proxy_host.setEnabled(True)
            self.proxy_port.setEnabled(True)
            self.proxy_login.setEnabled(True)
            self.proxy_password.setEnabled(True)
            self.change_ip_url.setEnabled(True)
        else:
            self.proxy_type.setEnabled(False)
            self.proxy_host.setEnabled(False)
            self.proxy_port.setEnabled(False)
            self.proxy_login.setEnabled(False)
            self.proxy_password.setEnabled(False)
            self.change_ip_url.setEnabled(False)

    def set_settings(self, emulator):
        emulator.set_path_to_ldplayer(self.ldplayer_path.text())
        emulator.set_smsactivate_api_key(self.sms_activate_api_key.text())
        emulator.set_country(self.country_number.currentText())
        emulator.set_proxy_type(self.proxy_type.currentText())
        emulator.set_proxy_host(self.proxy_host.text())
        emulator.set_proxy_port(self.proxy_port.text())
        emulator.set_proxy_login(self.proxy_login.text())
        emulator.set_proxy_password(self.proxy_password.text())
        emulator.set_number_of_profiles(self.num_of_profiles.text())
        emulator.set_change_ip_url(self.change_ip_url.text())
        emulator.set_geo(self.ldpayer_geo.currentText())
        emulator.set_loop_number(self.loop_numbers.isChecked())
        emulator.set_use_email(self.use_eamil.isChecked())
        emulator.set_use_proxy(self.use_proxy.isChecked())
        emulator.set_delete_dalvik_cache(self.delete_dalvik_cache.isChecked())
        emulator.set_emails_file(self.emails_list.text())

    # @pyqtSlot()
    def run_thread(self, emulator):
        #emulator = Emulator()
        if not AppiumServer.is_running():
            AppiumServer.start()
        self.set_settings(emulator)
        emulator.signals.finished.connect(self.thread_complete)
        self.thread_manager.start(emulator.run)
        # print("Number of Active Threads: " + str(self.thread_manager.activeThreadCount()))
        self.thread_manager.set_thread_running(True)

    def thread_complete(self):
        print("Thread Complete!\n")
        if self.thread_manager.activeThreadCount() == 0 and AppiumServer.is_running():
            AppiumServer.stop()
