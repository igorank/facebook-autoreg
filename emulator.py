import time
import random
from adb import AdbManager
from appium import webdriver
from fbsession import FBSession
from ldconsole import Ldconsole
from ipchanger import IPChanger
from imapreader import EmailReader
from filemanager import FileManager
from appiumserv import AppiumServer
from smsactivate.api import SMSActivateAPI
from PyQt6.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
from selenium.webdriver.common.action_chains import ActionChains, ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy
from appiumcommunicator import AppiumCommunicator
from randcoordgenerator import RandCoordGenerator
from randomnumgenerator import RandomNumGenerator
from randomuserpass import RandomGenerator


class EmulatorSignals(QObject):
    connected = pyqtSignal()
    finished = pyqtSignal()


class Emulator(QRunnable, AppiumCommunicator):
    CYRILLIC_COUNTRIES = ["RU", "UA", "BY", "BG", "KZ"]

    def __init__(self):
        super().__init__()
        self.fb_session = FBSession()
        self.ld_console = Ldconsole()
        self.signals = EmulatorSignals()
        self.random_coord_generator = RandCoordGenerator()
        self.title = None
        self.path_to_ldplayer = None  # C:\\LDPlayer\\LDPlayer4.0\\
        self.smsactivate_api_key = None
        self.emails_file = None
        self.proxy_type = None
        self.proxy_host = None
        self.proxy_port = None
        self.use_dynamic_port = None
        self.proxy_start_port = None
        self.proxy_end_port = None
        self.proxy_login = None
        self.proxy_password = None
        self.change_ip_url = None
        self.number_of_profiles = None
        self.country = None
        self.geo = None
        self.loop_numbers = None
        self.use_email = None
        self.use_proxy = None
        self.delete_dalvik_cache = None
        self.phone = None
        self.activation_id = None
        self.date_of_birth = None

    def set_number_of_profiles(self, num):
        self.number_of_profiles = int(num)

    def set_path_to_ldplayer(self, path):
        path_to_ldplayer = path
        length = len(path_to_ldplayer)
        last_char = path_to_ldplayer[length - 1]
        if last_char == '\\':
            self.path_to_ldplayer = r"{}".format(path_to_ldplayer)
        else:
            self.path_to_ldplayer = r"{}".format(path_to_ldplayer)
            self.path_to_ldplayer += '\\'

    def set_emails_file(self, path):
        self.emails_file = r"{}".format(path)

    def set_smsactivate_api_key(self, api_str):
        self.smsactivate_api_key = api_str

    def set_proxy_type(self, prx_type):
        self.proxy_type = prx_type

    def set_proxy_host(self, prx_host):
        self.proxy_host = prx_host

    def set_proxy_port(self, prx_port):
        if len(prx_port) == 0:
            self.proxy_port = None
        else:
            if '-' in prx_port:
                self.use_dynamic_port = True
                result = prx_port.partition("-")
                self.proxy_port = int(result[0])
                self.proxy_start_port = int(result[0])
                self.proxy_end_port = int(result[2])
            else:
                self.proxy_port = int(prx_port)

    def set_proxy_login(self, prx_login):
        self.proxy_login = prx_login

    def set_proxy_password(self, prx_pass):
        self.proxy_password = prx_pass

    def set_change_ip_url(self, url):
        self.change_ip_url = url

    def set_geo(self, country):
        self.geo = country

    def set_country(self, cntry):
        countries = {
            'RU': 0,
            'UA': 1,
            'KZ': 2,
            'PH': 4,
            'ID': 6,
            'MY': 7,
            'VN': 10,
            'KG': 11,
            'PL': 15,
            'GB': 16,
            'IN': 22,
            'EE': 34,
            'SK': 141
        }
        if cntry in countries:
            self.country = countries[cntry]

    def set_loop_number(self, boolean):
        self.loop_numbers = boolean

    def set_use_email(self, boolean):
        self.use_email = boolean

    def set_use_proxy(self, boolean):
        self.use_proxy = boolean

    def set_delete_dalvik_cache(self, boolean):
        self.delete_dalvik_cache = boolean

    @staticmethod
    def get_driver(number_of_attempts, desired_caps):
        it = 0
        while it < number_of_attempts:
            try:
                driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
                return driver
            except Exception as e:
                print(e)
                time.sleep(5)
                it += 1
        return False

    @staticmethod
    def get_status(sa, order_id):
        status = sa.getStatus(order_id)
        if status[0:9] != 'STATUS_OK':
            try:
                dict_status = sa.activationStatus(status)
                print(dict_status['message'])
            except:
                try:
                    time.sleep(3)
                    status = sa.getStatus(order_id)
                    dict_status = sa.activationStatus(status)
                    print(dict_status['message'])
                except:
                    sa.setStatus(id=order_id, status=8)
                    return "error"
        if status[0:9] == 'STATUS_OK':
            return status[10:16]
        else:
            return 0

    @staticmethod
    def exit(ldconsole, driver, title):
        try:
            driver.quit()
        except:
            pass
        ldconsole.quit(title)
        # ldconsole.remove(title)

    def change_port(self, driver, desried_caps, port):
        while True:
            if port >= self.proxy_end_port:
                self.proxy_port = self.proxy_start_port
            else:
                self.proxy_port += 1

            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, 'Droni')))
            driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Droni').click()
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((MobileBy.ID, 'org.sandrob.drony:id/toggleButtonOnOff')))
            driver.find_element(MobileBy.ID, 'org.sandrob.drony:id/toggleButtonOnOff').click()
            # self.find_element(driver, "id", "org.sandrob.drony:id/toggleButtonOnOff").click()
            self.swipe_right(actions)
            while self.check_right_swap_drony(driver) != 0:
                self.swipe_right(actions)
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((MobileBy.XPATH,
                                                  '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[8]/android.widget.RelativeLayout')))
            driver.find_element(MobileBy.XPATH,
                                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[8]/android.widget.RelativeLayout').click()
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((MobileBy.ID,
                                                  'org.sandrob.drony:id/network_list_item_id_name_value')))
            driver.find_element(MobileBy.ID,
                                'org.sandrob.drony:id/network_list_item_id_name_value').click()
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((MobileBy.XPATH,
                                                  '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[5]/android.widget.LinearLayout/android.widget.TextView[1]')))
            driver.find_element(MobileBy.XPATH,
                                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[6]/android.widget.LinearLayout/android.widget.TextView[1]').click()
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((MobileBy.XPATH,
                                                  '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText')))
            driver.find_element(MobileBy.XPATH,
                                '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText').clear()
            port_filed = driver.find_element(MobileBy.XPATH,
                                             '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText')

            while True:
                port_filed.send_keys(str(self.proxy_port))
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((MobileBy.ID,
                                                      'android:id/button1')))
                driver.find_element(MobileBy.ID,
                                    'android:id/button1').click()
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((MobileBy.XPATH,
                                                      '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[5]/android.widget.LinearLayout/android.widget.TextView[1]')))
                driver.find_element(MobileBy.XPATH,
                                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[6]/android.widget.LinearLayout/android.widget.TextView[1]').click()
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((MobileBy.XPATH,
                                                      '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText')))
                port_filed = driver.find_element(MobileBy.XPATH,
                                                 '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText')
                if port_filed.text == str(self.proxy_port):
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((MobileBy.ID,
                                                          'android:id/button1')))
                    driver.find_element(MobileBy.ID,
                                        'android:id/button1').click()
                    break
                else:
                    driver.find_element(MobileBy.XPATH,
                                        '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText').clear()
                    continue

            driver.back()
            time.sleep(2)
            driver.back()
            time.sleep(2)
            driver.back()
            self.swipe_left(actions)
            while self.check_left_swap_drony(driver) != 0:
                self.swipe_left(actions)
            self.find_element(driver, "id", "org.sandrob.drony:id/toggleButtonOnOff").click()
            time.sleep(4)
            driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_capabilities=desried_caps)
            time.sleep(8)
            driver.back()
            time.sleep(1)
            return driver

    def setup_drony(self, driver, desried_caps, wifi=True):
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, 'Droni')))
        driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Droni').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.ID, 'org.sandrob.drony:id/toggleButtonOnOff')))
        self.swipe_right(actions)
        while self.check_right_swap_drony(driver) != 0:
            self.swipe_right(actions)
        if wifi:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((MobileBy.XPATH,
                                                  '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[8]/android.widget.RelativeLayout')))
            driver.find_element(MobileBy.XPATH,
                                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[8]/android.widget.RelativeLayout').click()
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((MobileBy.ID,
                                                  'org.sandrob.drony:id/network_list_item_id_name_value')))
            driver.find_element(MobileBy.ID,
                                'org.sandrob.drony:id/network_list_item_id_name_value').click()
        else:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((MobileBy.XPATH,
                                                  '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[9]/android.widget.RelativeLayout/android.widget.TextView')))
            driver.find_element(MobileBy.XPATH,
                                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[9]/android.widget.RelativeLayout/android.widget.TextView').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[5]/android.widget.LinearLayout/android.widget.TextView[1]')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[5]/android.widget.LinearLayout/android.widget.TextView[1]').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText').send_keys(
            self.proxy_host)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.ID,
                                              'android:id/button1')))
        driver.find_element(MobileBy.ID,
                            'android:id/button1').click()
        # self.find_element(driver, "id", "android:id/button1").click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[6]/android.widget.LinearLayout/android.widget.TextView[1]')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[6]/android.widget.LinearLayout/android.widget.TextView[1]').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText').send_keys(
            self.proxy_port)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.ID,
                                              'android:id/button1')))
        driver.find_element(MobileBy.ID,
                            'android:id/button1').click()
        # self.find_element(driver, "id", "android:id/button1").click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[7]/android.widget.LinearLayout/android.widget.TextView[1]')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[7]/android.widget.LinearLayout/android.widget.TextView[1]').click()
        # self.find_element(driver, "xpath",
        #                   "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[7]/android.widget.LinearLayout/android.widget.TextView[1]").click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText').send_keys(
            self.proxy_login)
        # self.find_element(driver, "xpath",
        #                   "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText").send_keys(
        #     self.proxy_login)  # login
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.ID,
                                              'android:id/button1')))
        driver.find_element(MobileBy.ID,
                            'android:id/button1').click()
        # self.find_element(driver, "id", "android:id/button1").click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[8]/android.widget.LinearLayout/android.widget.TextView[1]')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[8]/android.widget.LinearLayout/android.widget.TextView[1]').click()
        # self.find_element(driver, "xpath",
        #                   "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[8]/android.widget.LinearLayout/android.widget.TextView[1]").click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText').send_keys(
            self.proxy_password)
        # self.find_element(driver, "xpath",
        #                   "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText").send_keys(
        #     self.proxy_password)  # password
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.ID,
                                              'android:id/button1')))
        driver.find_element(MobileBy.ID,
                            'android:id/button1').click()
        # self.find_element(driver, "id", "android:id/button1").click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[8]/android.widget.LinearLayout/android.widget.TextView[1]')))
        # time.sleep(2)
        self.swipe_down(actions)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[9]/android.widget.LinearLayout/android.widget.TextView[1]')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[9]/android.widget.LinearLayout/android.widget.TextView[1]').click()
        # self.find_element(driver, "xpath",
        #                   "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[9]/android.widget.LinearLayout/android.widget.TextView[1]").click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[4]')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[4]').click()
        # self.find_element(driver, "xpath",
        #                   "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[4]").click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[9]/android.widget.LinearLayout/android.widget.TextView[1]')))
        # time.sleep(2)
        driver.back()
        if wifi:
            time.sleep(1)
            driver.back()
        time.sleep(3)
        self.swipe_left(actions)
        while self.check_left_swap_drony(driver) != 0:
            self.swipe_left(actions)
        self.find_element(driver, "id", "org.sandrob.drony:id/toggleButtonOnOff").click()
        try:
            self.find_element(driver, "id", "android:id/button1").click()
        except:
            pass
        time.sleep(4)
        driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_capabilities=desried_caps)
        time.sleep(8)
        driver.back()
        time.sleep(1)
        return driver

    def facebook_lite_reg(self, driver, name, surname, password, num_or_email=None, use_email=False):
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        try:
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, 'Lite')))
            driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Lite').click()
            try:
                WebDriverWait(driver, 25).until(
                    EC.visibility_of_element_located(
                        (MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button')))
            except:
                print("Failed to initialize Facebook Lite. Check Internet connection")
                raise Exception
            driver.find_element(MobileBy.ID, 'com.android.packageinstaller:id/permission_deny_button').click()
            self.find_element(driver, "xpath",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.View",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.View").click()
            self.find_element(driver, "xpath",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup").click()
            self.find_element(driver, "xpath",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView[1]",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView[1]").send_keys(
                name)
            while True:
                try:
                    driver.find_element(MobileBy.XPATH,
                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView[2]').send_keys(
                        surname)
                    break
                except:
                    try:
                        driver.find_element(MobileBy.XPATH,
                                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView[2]').send_keys(
                            surname)
                        break
                    except:
                        continue
            # self.find_element(driver, "xpath",
            #                   "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView[2]",
            #                   "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView[2]").send_keys(
            #     surname)
            while True:
                try:
                    driver.find_element(MobileBy.XPATH,
                                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup").click()
                    break
                except:
                    try:
                        driver.find_element(MobileBy.XPATH,
                                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup").click()
                        break
                    except:
                        continue
            # self.find_element(driver, "xpath",
            #                   "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup",
            #                   "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup").click()  # next
            # self.find_element(driver, "id", "com.android.packageinstaller:id/permission_allow_button").click()  # allow
            for i in range(3):
                self.find_element(driver, "id", "com.android.packageinstaller:id/permission_deny_button").click()
            if use_email:
                self.find_element(driver, "xpath",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.View",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.View").click()  # зарег с помощью почты кнопка
                self.find_element(driver, "xpath",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView").send_keys(
                    num_or_email)  # email field
                self.find_element(driver, "xpath",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]").click()  # Next Button
            else:
                # self.find_element(driver, "xpath",
                #                   "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView",
                #                   "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView").clear()  # clear phone field
                self.find_element(driver, "xpath",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView").send_keys(
                    self.phone)  # phone number
                self.find_element(driver, "xpath",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]").click()  # next button
            if self.date_field_available(driver):
                day = self.send_day_facebooklite(driver)
                month = self.send_month_facebooklite(driver)
                year = self.send_year_facebooklite(driver)
                self.date_of_birth = day + "." + month + "." + year
            else:
                return 0
            self.find_element(driver, "xpath",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[2]",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup[2]").click()  # next
            WebDriverWait(driver, 40).until(EC.any_of(
                EC.element_to_be_clickable((MobileBy.XPATH,
                                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.View[1]")),
                EC.element_to_be_clickable((MobileBy.XPATH,
                                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.View[1]"))
            ))
            self.find_element(driver, "xpath",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.View[1]",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.View[1]").click()  # female text
            if self.password_field_available(driver):
                time.sleep(1)
                self.delay_send(actions, password, random.uniform(0.05, 0.1))
                time.sleep(1)
            else:
                return 0
            self.find_element(driver, "xpath",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup").click()  # next
            self.find_element(driver, "xpath",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[7]",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[7]",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[5]",
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[5]").click()  # registration (/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[7] old), "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[7]"
        except NameError as ne:
            print(ne)
            return -1
        except ValueError as e:
            print(e)
            return 0
        if self.check_checkpoint_lite(driver) == 0:
            return 1
        else:
            return 0

    def get_mobile_code(self, sa, driver, order_id, delay):
        attempts_get_code = 0
        while True:
            code = self.get_status(sa, order_id)
            if code != 0:
                break
            if (code == "error") or (attempts_get_code > delay):  # defaul: attempts_get_code > 7
                sa.setStatus(id=order_id,
                             status=8)  # сообщить о том, что номер использован и отменить активацию
                break
            else:
                try:
                    if driver.find_element_by_xpath(
                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup"):
                        self.find_element(driver, "xpath",
                                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.View[3]",
                                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.View[3]").click()
                except:
                    pass
            attempts_get_code = attempts_get_code + 1
            time.sleep(10)
        if (code != "error") and (attempts_get_code <= delay):  # defaul: attempts_get_code <= 7
            return code
        else:
            print("SMS did not come")
            return 0

    def verify_fblite_by_mob(self, driver, code):
        self.find_element(driver, "xpath",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView").click()  # inpute code field
        self.find_element(driver, "xpath",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView").send_keys(
            str(code))
        self.find_element(driver, "xpath",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]").click()

    def get_number(self, sa):
        sa_number = sa.getNumber(service='fb', country=self.country)
        try:
            number = sa_number['phone']
            return sa_number
        except:
            print("No numbers")
            return 0

    def get_pnumber(self, sa):
        if self.loop_numbers:
            sa_number = 0
            while sa_number == 0:
                sa_number = self.get_number(sa)
                time.sleep(2)
            return sa_number
        else:
            sa_number = self.get_number(sa)  # BUG?
            if sa_number == 0:
                return False
            else:
                return sa_number

    def get_fbdata(self, num_or_email, phone, password, filename):
        """
        Заходит через прокси в аккаунт и вытягивает cookies, token. Затем записывает эти данные в аргумент filename.
        """
        username = num_or_email if self.use_email else phone
        useragent, cookies, token = self.fb_session.get_data(str(username), password,
                                                             self.proxy_login,
                                                             self.proxy_password, self.proxy_host,
                                                             self.proxy_port)
        file = open(filename, "a")
        file.write(str(useragent) + ";" + str(cookies) + ";" + str(token) + ";\n")
        file.close()
        # return useragent, cookies, token

    def get_names(self, names, surnames, names_eng, surnames_eng):
        if self.geo in Emulator.CYRILLIC_COUNTRIES:
            name = names[random.randint(0, 197)]
            surname = surnames[random.randint(0, 197)]
        else:
            name = names_eng[random.randint(0, 98)]
            surname = surnames_eng[random.randint(0, 98)]
        return name, surname

    def get_mailornum(self, emails, num, sa):
        if self.use_email:
            num_or_email = emails[num].partition(";")[0]
        else:
            num_or_email = self.get_pnumber(sa)
            self.phone = num_or_email['phone']
            self.activation_id = num_or_email['activation_id']
        return num_or_email

    @pyqtSlot()
    def run(self):
        self.ld_console.set_path(self.path_to_ldplayer)
        sa = SMSActivateAPI(self.smsactivate_api_key)
        sa.debug_mode = True  # TEMP?

        names = FileManager.get_filesdata('names\\names.txt')
        surnames = FileManager.get_filesdata('names\\surnames.txt')
        names_eng = FileManager.get_filesdata('names\\names_eng.txt')
        surnames_eng = FileManager.get_filesdata('names\\surnames_eng.txt')

        if self.use_email:
            try:
                emails = FileManager.get_filesdata(self.emails_file, True)
                random.shuffle(emails)  # reorganize the order of the list items
            except Exception as e:
                print(f"Unable to open file {str(self.emails_file)}: " + str(e))
                AppiumServer.forced_stop()
                self.signals.finished.emit()
                return
            self.number_of_profiles = len(emails)
        else:
            emails = 0

        self.title = RandomGenerator.random_username(8)  # рвндомное название плеера
        self.ld_console.add(self.title)  # создаем плеер

        n_cord, e_cord = self.random_coord_generator.get_rand_coord(self.geo)

        profile_index = self.ld_console.get_profile_index(self.title)
        line = self.ld_console.find_num_of_line(profile_index)
        self.ld_console.set_debug_mode(profile_index, line)
        self.ld_console.set_location(profile_index, line, cord_n=n_cord, cord_e=e_cord)

        number = RandomNumGenerator.get_rand_mob_num()
        self.ld_console.modify(self.title, str(number))

        self.ld_console.launch(self.title)
        time.sleep(10)  # TEMP

        while True:
            current_device = AdbManager.get_list_difference(AdbManager.get_connected_devices(),
                                                            AdbManager.get_list_of_launched_devices())
            if len(current_device):
                AdbManager.add_index_to_dic(profile_index, current_device[0])
                AdbManager.add_launched_device(current_device[0])
                break
            else:
                time.sleep(3)

        caps = {"platformName": "Android", "udid": str(AdbManager.get_dict_value_by_key(profile_index)),
                "newCommandTimeout": 99999}

        driver = self.get_driver(3, caps)
        if not driver:
            self.exit(self.ld_console, driver, self.title)
            IPChanger.change_ip(self.change_ip_url)
            AdbManager.delete_index_from_dict(profile_index)
            AdbManager.remove_launched_device(current_device[0])
            self.signals.finished.emit()
            return 1

        print("Profile " + str(self.title) + " has been connected to Appium\n")
        self.signals.connected.emit()

        if self.use_proxy:
            self.ld_console.install_app(self.title, app_name=r'apps\drony.apk')
            while True:  # пока дрони не инициализируется
                try:
                    driver = self.setup_drony(driver, caps)
                    break
                except:
                    AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                               "shell am force-stop org.sandrob.drony")
                    AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                               "shell pm clear org.sandrob.drony")

        self.ld_console.install_app(self.title, app_name=r'apps\facebook_lite_v320.0.0.12.108.apk')

        for i in range(self.number_of_profiles):
            try:
                num_or_email = self.get_mailornum(emails, i, sa)
                if not num_or_email:
                    break
                name, surname = self.get_names(names, surnames, names_eng, surnames_eng)
                password = RandomGenerator.random_password(random.randint(12, 16))
                reg_status = self.facebook_lite_reg(driver, name, surname, password, num_or_email,
                                                    use_email=self.use_email)
                if reg_status == 1:
                    if self.use_email:
                        mail_reader = EmailReader("mail.inbox.lv", num_or_email,
                                                  emails[i].partition(";")[2].partition(";")[2].partition(";")[0])
                        code = mail_reader.get_facebook_code(300)  # аргумент - задержка
                        FileManager.remove_line_by_text(self.emails_file,
                                                        str(num_or_email))  # удаляем почту из txt файла
                    else:
                        code = self.get_mobile_code(sa, driver, self.activation_id, 8)  # получаем код на номер
                    if code != 0:
                        self.verify_fblite_by_mob(driver, code)
                        file = open("autoregs_emu.txt", "a")
                        fb_username = num_or_email if self.use_email else self.phone
                        file.write(str(fb_username) + ";" + password + ";")
                        if self.use_email:
                            file.write(emails[i].partition(";")[2].partition(";")[0] + ";")  # write email password
                        file.write(name + " " + surname + ";" + self.date_of_birth + ";")
                        file.close()
                        if self.check_registration(driver, self.use_email):
                            try:
                                self.get_fbdata(num_or_email, self.phone, password, "autoregs_emu.txt")
                            except Exception as e:
                                print(e)
                                file = open("autoregs_emu.txt", "a")
                                file.write("\n")
                                file.close()
                            if not self.use_email:
                                sa.setStatus(id=self.activation_id, status=6)  # завершить активацию
                        else:
                            file = open("autoregs_emu.txt", "a")
                            file.write("\n")
                            file.close()
                        driver.terminate_app('com.facebook.lite')
                        AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                                   "shell pm clear com.facebook.lite")
                        if self.delete_dalvik_cache:
                            AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                                       "shell rm -r /data/dalvik-cache")
                            AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                                       "shell rm -r /cache/dalvik-cache")
                        self.ld_console.randomize_settings(profile_index, self.geo, self.delete_dalvik_cache)
                        if self.use_proxy:
                            if len(self.change_ip_url) == 0 and self.use_dynamic_port:
                                driver = self.change_port(driver, caps, self.proxy_port)
                            else:
                                IPChanger.change_ip(self.change_ip_url)
                    else:
                        if not self.use_email:
                            sa.setStatus(id=self.activation_id,
                                         status=8)  # сообщить о том, что номер использован и отменить активацию
                        driver.terminate_app('com.facebook.lite')
                        AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                                   "shell pm clear com.facebook.lite")
                        if self.delete_dalvik_cache:
                            AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                                       "shell rm -r /data/dalvik-cache")
                            AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                                       "shell rm -r /cache/dalvik-cache")
                        self.ld_console.randomize_settings(profile_index, self.geo, self.delete_dalvik_cache)
                        if self.use_proxy:
                            if len(self.change_ip_url) == 0 and self.use_dynamic_port:
                                driver = self.change_port(driver, caps, self.proxy_port)
                            else:
                                IPChanger.change_ip(self.change_ip_url)
                elif reg_status == 0:
                    if not self.use_email:
                        sa.setStatus(id=self.activation_id,
                                     status=8)  # сообщить о том, что номер использован и отменить активацию
                    if driver.query_app_state("com.android.chrome") == 4:
                        self.close_chrome(driver)
                    driver.terminate_app('com.facebook.lite')
                    AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                               "shell pm clear com.facebook.lite")
                    if self.delete_dalvik_cache:
                        AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                                   "shell rm -r /data/dalvik-cache")
                        AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                                   "shell rm -r /cache/dalvik-cache")
                    self.ld_console.randomize_settings(profile_index, self.geo, self.delete_dalvik_cache)
                    if self.use_proxy:
                        if len(self.change_ip_url) == 0 and self.use_dynamic_port:
                            driver = self.change_port(driver, caps, self.proxy_port)
                        else:
                            IPChanger.change_ip(self.change_ip_url)
                elif reg_status == -1:
                    break
            except Exception as e:
                # print('Failed. ' + str(e))
                # print('Failed.')
                if not self.use_email:
                    sa.setStatus(id=self.activation_id,
                                 status=8)  # сообщить о том, что номер использован и отменить активацию
                if driver.query_app_state("com.android.chrome") == 4:
                    self.close_chrome(driver)
                driver.terminate_app('com.facebook.lite')
                AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                           "shell pm clear com.facebook.lite")
                if self.delete_dalvik_cache:
                    AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                               "shell rm -r /data/dalvik-cache")
                    AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                               "shell rm -r /cache/dalvik-cache")
                self.ld_console.randomize_settings(profile_index, self.geo, self.delete_dalvik_cache)
                if self.use_proxy:
                    if len(self.change_ip_url) == 0 and self.use_dynamic_port:
                        driver = self.change_port(driver, caps, self.proxy_port)
                    else:
                        IPChanger.change_ip(self.change_ip_url)
                continue
        self.exit(self.ld_console, driver, self.title)
        AdbManager.delete_index_from_dict(profile_index)
        AdbManager.remove_launched_device(current_device[0])
        self.signals.finished.emit()