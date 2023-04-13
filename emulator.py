import time
import random
from selenium.webdriver.common.action_chains import ActionChains, ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from smsactivate.api import SMSActivateAPI
from PyQt6.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
from adb import AdbManager
# from fbsession import FBSession
# from fbsession import FBSession
from ldconsole import Ldconsole
from ipchanger import IPChanger
from imapreader import EmailReader
from filemanager import FileManager
from appiumserv import AppiumServer
from randcoordgenerator import RandCoordGenerator
from randomnumgenerator import RandomNumGenerator
from randomuserpass import RandomGenerator
from facebooklite import FacebookLite, find_element


class EmulatorSignals(QObject):
    connected = pyqtSignal()
    finished = pyqtSignal()


class Emulator(QRunnable):
    CYRILLIC_COUNTRIES = ["RU", "UA", "BY", "BG", "KZ"]

    def __init__(self):
        super().__init__()
        # self.fb_session = FBSession()
        self.ld_console = Ldconsole()
        self.signals = EmulatorSignals()
        self.random_coord_generator = RandCoordGenerator()
        self.__title = None
        self.__path_to_ldplayer = None  # C:\\LDPlayer\\LDPlayer4.0\\
        self.__smsactivate_api_key = None
        self.__emails_file = None
        self.__proxy = None
        self.__number_of_profiles = None
        self.__country = None
        self.__geo = None
        self.__loop_numbers = None
        self.__use_email = None
        self.__use_proxy = None
        self.__delete_dalvik_cache = None
        self.__phone = None
        self.__activation_id = None

    def set_number_of_profiles(self, num):
        self.__number_of_profiles = int(num)

    def set_path_to_ldplayer(self, path):
        path_to_ldplayer = path
        length = len(path_to_ldplayer)
        last_char = path_to_ldplayer[length - 1]
        if last_char == '\\':
            self.__path_to_ldplayer = r"{}".format(path_to_ldplayer)
        else:
            self.__path_to_ldplayer = r"{}".format(path_to_ldplayer)
            self.__path_to_ldplayer += '\\'

    def set_emails_file(self, path):
        self.__emails_file = r"{}".format(path)

    def set_smsactivate_api_key(self, api_str):
        self.__smsactivate_api_key = api_str

    def set_proxy_settings(self, prx_type, prx_host, prx_login,
                           prx_pass, prx_port, url):

        if len(prx_port) == 0:
            proxy_port = None
            self.__proxy = {'type': prx_type, 'host': prx_host, 'login': prx_login,
                            'password': prx_pass, 'port': proxy_port, 'change_ip_url': url}
        else:
            if '-' in prx_port:
                use_dynamic_port = True
                result = prx_port.partition("-")
                proxy_port = int(result[0])
                proxy_start_port = int(result[0])
                proxy_end_port = int(result[2])
                self.__proxy = {'type': prx_type, 'host': prx_host, 'login': prx_login,
                                'password': prx_pass, 'port': proxy_port, 'change_ip_url': url,
                                'dynamic_port': use_dynamic_port, 'start_port': proxy_start_port,
                                'end_port': proxy_end_port}
            else:
                proxy_port = int(prx_port)
                self.__proxy = {'type': prx_type, 'host': prx_host, 'login': prx_login,
                                'password': prx_pass, 'port': proxy_port, 'change_ip_url': url}

    def set_geo(self, country):
        self.__geo = country

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
            self.__country = countries[cntry]

    def set_loop_number(self, boolean):
        self.__loop_numbers = boolean

    def set_use_email(self, boolean):
        self.__use_email = boolean

    def set_use_proxy(self, boolean):
        self.__use_proxy = boolean

    def set_delete_dalvik_cache(self, boolean):
        self.__delete_dalvik_cache = boolean

    @staticmethod
    def __get_driver(number_of_attempts, desired_caps):
        for _ in range(number_of_attempts):
            try:
                driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
                return driver
            except Exception as exception:
                print(exception)
                time.sleep(5)
        return False

    @staticmethod
    def get_status(sms_act, order_id):
        status = sms_act.getStatus(order_id)
        if status[0:9] != 'STATUS_OK':
            try:
                dict_status = sms_act.activationStatus(status)
                print(dict_status['message'])
            except:
                try:
                    time.sleep(3)
                    status = sms_act.getStatus(order_id)
                    dict_status = sms_act.activationStatus(status)
                    print(dict_status['message'])
                except:
                    sms_act.setStatus(id=order_id, status=8)
                    return "error"
        if status[0:9] == 'STATUS_OK':
            return status[10:16]
        return 0

    @staticmethod
    def __exit(ldconsole, driver, title):
        try:
            driver.quit()
        except:
            pass
        ldconsole.quit(title)

    def __change_port(self, driver, desried_caps, port):
        while True:
            if port >= self.__proxy['end_port']:
                self.__proxy['port'] = self.__proxy['start_port']
            else:
                self.__proxy['port'] += 1

            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, 'Droni')))
            driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Droni').click()
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((MobileBy.ID, 'org.sandrob.drony:id/toggleButtonOnOff')))
            driver.find_element(MobileBy.ID, 'org.sandrob.drony:id/toggleButtonOnOff').click()
            self.__swipe_right(actions)
            while self.__check_right_swap_drony(driver) != 0:
                self.__swipe_right(actions)
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
                port_filed.send_keys(str(self.__proxy['port']))
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
                if port_filed.text == str(self.__proxy['port']):
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((MobileBy.ID,
                                                          'android:id/button1')))
                    driver.find_element(MobileBy.ID,
                                        'android:id/button1').click()
                    break
                driver.find_element(MobileBy.XPATH,
                                    '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText').clear()
                continue

            driver.back()
            time.sleep(2)
            driver.back()
            time.sleep(2)
            driver.back()
            self.__swipe_left(actions)
            while self.__check_left_swap_drony(driver) != 0:
                self.__swipe_left(actions)
            find_element(driver, "id", "org.sandrob.drony:id/toggleButtonOnOff").click()
            time.sleep(4)
            driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_capabilities=desried_caps)
            time.sleep(8)
            driver.back()
            time.sleep(1)
            return driver

    def __setup_drony(self, driver, desried_caps, wifi=True):
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, 'Droni')))
        driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Droni').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.ID, 'org.sandrob.drony:id/toggleButtonOnOff')))
        self.__swipe_right(actions)
        while self.__check_right_swap_drony(driver) != 0:
            self.__swipe_right(actions)
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
            self.__proxy['host'])
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.ID,
                                              'android:id/button1')))
        driver.find_element(MobileBy.ID,
                            'android:id/button1').click()
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
            self.__proxy['port'])
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.ID,
                                              'android:id/button1')))
        driver.find_element(MobileBy.ID,
                            'android:id/button1').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[7]/android.widget.LinearLayout/android.widget.TextView[1]')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[7]/android.widget.LinearLayout/android.widget.TextView[1]').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText').send_keys(
            self.__proxy['login'])
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.ID,
                                              'android:id/button1')))
        driver.find_element(MobileBy.ID,
                            'android:id/button1').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[8]/android.widget.LinearLayout/android.widget.TextView[1]')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[8]/android.widget.LinearLayout/android.widget.TextView[1]').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.EditText').send_keys(
            self.__proxy['password'])
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.ID,
                                              'android:id/button1')))
        driver.find_element(MobileBy.ID,
                            'android:id/button1').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[8]/android.widget.LinearLayout/android.widget.TextView[1]')))
        self.__swipe_down(actions)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[9]/android.widget.LinearLayout/android.widget.TextView[1]')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[9]/android.widget.LinearLayout/android.widget.TextView[1]').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[4]')))
        driver.find_element(MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[4]').click()
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[9]/android.widget.LinearLayout/android.widget.TextView[1]')))
        # time.sleep(2)
        driver.back()
        if wifi:
            time.sleep(1)
            driver.back()
        time.sleep(3)
        self.__swipe_left(actions)
        while self.__check_left_swap_drony(driver) != 0:
            self.__swipe_left(actions)
        find_element(driver, "id", "org.sandrob.drony:id/toggleButtonOnOff").click()
        try:
            find_element(driver, "id", "android:id/button1").click()
        except NoSuchElementException:
            pass
        time.sleep(4)
        driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_capabilities=desried_caps)
        time.sleep(8)
        driver.back()
        time.sleep(1)
        return driver

    def __get_mobile_code(self, sms_act, driver, order_id, delay):
        attempts_get_code = 0
        while True:
            code = self.get_status(sms_act, order_id)
            if code != 0:
                break
            if (code == "error") or (attempts_get_code > delay):  # defaul: attempts_get_code > 7
                sms_act.setStatus(id=order_id,
                                  status=8)  # сообщить о том, что номер использован и отменить активацию
                break
            try:
                if driver.find_element(MobileBy.XPATH,
                                       "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup"):
                    find_element(driver, "xpath",
                                 "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.View[3]",
                                 "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.View[3]").click()
            except NoSuchElementException:
                pass
            attempts_get_code = attempts_get_code + 1
            time.sleep(10)
        if (code != "error") and (attempts_get_code <= delay):  # defaul: attempts_get_code <= 7
            return code
        print("SMS did not come")
        return 0

    @staticmethod
    def __verify_fblite_by_mob(driver, code):
        find_element(driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView").click()  # inpute code field
        find_element(driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView").send_keys(
            str(code))
        find_element(driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup[1]",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]").click()

    def __get_number(self, sms_act):
        sa_number = sms_act.getNumber(service='fb', country=self.__country)
        try:
            number = sa_number['phone']
            return sa_number
        except:
            print("No numbers")
            return 0

    def __get_pnumber(self, sms_act):

        if self.__loop_numbers:
            sa_number = 0
            while sa_number == 0:
                sa_number = self.__get_number(sms_act)
                time.sleep(2)
            return sa_number

        sa_number = self.__get_number(sms_act)  # BUG?
        if sa_number == 0:
            return False
        return sa_number

    # def __get_fbdata(self, num_or_email, phone, password, filename):
    #     """
    #     Заходит через прокси в аккаунт и вытягивает cookies, token. Затем записывает эти данные в аргумент filename.
    #     """
    #     username = num_or_email if self.use_email else phone
    #     useragent, cookies, token = self.fb_session.get_data(str(username), password,
    #                                                          self.proxy_login,
    #                                                          self.proxy_password, self.proxy_host,
    #                                                          self.proxy_port)
    #     with open(filename, "a") as file:
    #         file.write(str(useragent) + ";" + str(cookies) + ";" + str(token) + ";\n")
    #     # return useragent, cookies, token

    def __get_names(self, names, surnames, names_eng, surnames_eng):
        if self.__geo in Emulator.CYRILLIC_COUNTRIES:
            name = names[random.randint(0, 197)]
            surname = surnames[random.randint(0, 197)]
        else:
            name = names_eng[random.randint(0, 98)]
            surname = surnames_eng[random.randint(0, 98)]
        return name, surname

    def __get_mailornum(self, emails, num, sms_act):
        if self.__use_email:
            num_or_email = emails[num].partition(";")[0]
        else:
            num_or_email = self.__get_pnumber(sms_act)
            self.__phone = num_or_email['phone']
            self.__activation_id = num_or_email['activation_id']
        return num_or_email

    @staticmethod
    def __check_right_swap_drony(driver):
        while True:
            if driver.find_element(by=MobileBy.XPATH,
                                   value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[8]/android.widget.RelativeLayout"):
                return 0
            time.sleep(3)

    @staticmethod
    def __check_left_swap_drony(driver):
        while True:
            if driver.find_element(MobileBy.ID, "org.sandrob.drony:id/toggleButtonOnOff"):
                return 0
            time.sleep(3)

    @staticmethod
    def __swipe_right(actions):
        actions.w3c_actions.pointer_action.move_to_location(522, 480)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(17, 475)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    @staticmethod
    def __swipe_left(actions):
        actions.w3c_actions.pointer_action.move_to_location(11, 529)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(522, 534)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    @staticmethod
    def __swipe_down(actions):
        actions.w3c_actions.pointer_action.move_to_location(264, 791)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(268, 630)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    @staticmethod
    def __check_registration(driver, use_email=False) -> bool:
        for _ in range(45):
            if not use_email:
                try:
                    # BUG
                    if driver.find_element(MobileBy.XPATH,
                                           "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.View[2]"):
                        print("Profile verified")
                        return True
                except NoSuchElementException:
                    pass
            else:
                pass
            try:
                if driver.find_element(MobileBy.XPATH,
                                       "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.View[2]"):
                    print("Profile verified")
                    return True
            except NoSuchElementException:
                pass
            try:
                if driver.find_element(MobileBy.XPATH,
                                       "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.View[2]"):
                    print("Profile verified")
                    return True
            except NoSuchElementException:
                pass
            try:
                driver.find_element(MobileBy.XPATH,
                                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.View[3]').click()  # "произошла ошибка"
                find_element(driver, "xpath",
                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]",
                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]").click()
            except NoSuchElementException:
                pass
            time.sleep(2)
        print("Error. Profile has not been verified")
        return False

    @staticmethod
    def __get_device(prof_index):
        while True:
            current_device = AdbManager.get_list_difference(AdbManager.get_connected_devices(),
                                                            AdbManager.get_list_of_launched_devices())
            if len(current_device):
                AdbManager.add_index_to_dic(prof_index, current_device[0])
                AdbManager.add_launched_device(current_device[0])
                return current_device[0]
            time.sleep(3)

    def __init_drony(self, driver, caps, prof_indx):
        while True:  # пока дрони не инициализируется
            try:
                driver = self.__setup_drony(driver, caps)
                return driver
            except Exception as exception:
                print(exception)
                AdbManager.execute_command(AdbManager.get_dict_value_by_key(prof_indx),
                                           "shell am force-stop org.sandrob.drony")
                AdbManager.execute_command(AdbManager.get_dict_value_by_key(prof_indx),
                                           "shell pm clear org.sandrob.drony")

    def __get_code(self, driver, sms_activate, num_or_email, email):
        if self.__use_email:
            mail_reader = EmailReader("mail.inbox.lv", num_or_email,
                                      email.partition(";")[2].partition(";")[2].partition(";")[0])
            code = mail_reader.get_facebook_code(300)  # аргумент - задержка
            FileManager.remove_line_by_text(self.__emails_file,
                                            str(num_or_email))  # удаляем почту из txt файла
        else:
            code = self.__get_mobile_code(sms_activate, driver, self.__activation_id,
                                          8)  # получаем код на номер
        return code

    def __write_file(self, num_or_email, passw, email, name, surname, date_of_birth):
        with open("autoregs_emu.txt", "a") as file:
            fb_username = num_or_email if self.__use_email else self.__phone
            file.write(str(fb_username) + ";" + passw + ";")
            if self.__use_email:
                file.write(email.partition(";")[2].partition(";")[0] + ";")  # write email password
            file.write(name + " " + surname + ";" + date_of_birth + ";\n")

    def __proxy_check(self, driver, caps):
        if self.__use_proxy:
            if len(self.__proxy['change_ip_url']) == 0 and self.__proxy['dynamic_port']:
                driver = self.__change_port(driver, caps, self.__proxy['port'])
                return driver
            IPChanger.change_ip(self.__proxy['change_ip_url'])
        return driver

    def __unsuc_reg(self, driver, sms_activate, profile_index, caps):
        if not self.__use_email:
            sms_activate.setStatus(id=self.__activation_id,
                                   status=8)  # сообщить о том, что номер использован и отменить активацию
        if driver.query_app_state("com.android.chrome") == 4:
            driver.terminate_app('com.android.chrome')
        self.__close_fb_app(driver, profile_index)
        if self.__delete_dalvik_cache:
            AdbManager.del_dalvik(profile_index)
        self.ld_console.randomize_settings(profile_index, self.__geo, self.__delete_dalvik_cache)
        driver = self.__proxy_check(driver, caps)
        return driver

    @staticmethod
    def __write_newl():
        with open("autoregs_emu.txt", "a") as file:
            file.write("\n")

    def __terminate(self, driver, device, profile_index):
        self.__exit(self.ld_console, driver, self.__title)
        IPChanger.change_ip(self.__proxy['change_ip_url'])
        AdbManager.delete_index_from_dict(profile_index)
        AdbManager.remove_launched_device(device)

    def __get_emails(self):
        if self.__use_email:
            try:
                emails = FileManager.get_filesdata(self.__emails_file, True)
                random.shuffle(emails)  # reorganize the order of the list items
                self.__number_of_profiles = len(emails)
                return emails
            except Exception as exception:
                print(f"Unable to open file {str(self.__emails_file)}: " + str(exception))
                AppiumServer.forced_stop()
                return None
        else:
            # emails = 0
            return []

    @staticmethod
    def __get_profile_data() -> list:
        names = FileManager.get_filesdata('names\\names.txt')
        surnames = FileManager.get_filesdata('names\\surnames.txt')
        names_eng = FileManager.get_filesdata('names\\names_eng.txt')
        surnames_eng = FileManager.get_filesdata('names\\surnames_eng.txt')
        return [names, surnames, names_eng, surnames_eng]

    def __finish_reg(self, driver, sms_activate):
        if self.__check_registration(driver, self.__use_email):
            self.__write_newl()
            # try:
            #     self.__get_fbdata(num_or_email, self.phone, password, "autoregs_emu.txt")
            # except Exception as exception:
            #     print(exception)
            #     self.__write_newl()
            if not self.__use_email:
                sms_activate.setStatus(id=self.__activation_id, status=6)  # завершить активацию
        else:
            self.__write_newl()

    def __after_closing(self, profile_index):
        if self.__delete_dalvik_cache:
            AdbManager.del_dalvik(profile_index)
        self.ld_console.randomize_settings(profile_index, self.__geo, self.__delete_dalvik_cache)

    @staticmethod
    def __close_fb_app(driver, profile_index):
        driver.terminate_app('com.facebook.lite')
        AdbManager.execute_command(AdbManager.get_dict_value_by_key(profile_index),
                                   "shell pm clear com.facebook.lite")

    def __loop(self, driver, sms_activate, prof_data, emails, profile_index):
        for i in range(self.__number_of_profiles):
            try:
                num_or_email = self.__get_mailornum(emails, i, sms_activate)
                if not num_or_email:
                    break

                name, surname = self.__get_names(prof_data[0], prof_data[1], prof_data[2], prof_data[3])
                password = RandomGenerator.random_password(random.randint(12, 16))
                profile_data = {'name': name, 'surname': surname, 'password': password}

                facebookl = FacebookLite(driver['driver'], self.__phone)
                reg_status = facebookl.register(profile_data, num_or_email, use_email=self.__use_email)

                if isinstance(reg_status, str):
                    code = self.__get_code(driver['driver'], sms_activate, num_or_email, emails[i])
                    if code != 0:
                        self.__verify_fblite_by_mob(driver['driver'], code)
                        self.__write_file(num_or_email, password, emails[i],
                                          name, surname, reg_status)
                        self.__finish_reg(driver['driver'], sms_activate)
                        self.__close_fb_app(driver['driver'], profile_index)
                        self.__after_closing(profile_index)
                        driver['driver'] = self.__proxy_check(driver['driver'], driver['caps'])
                    else:
                        if not self.__use_email:
                            sms_activate.setStatus(id=self.__activation_id,
                                                   status=8)  # сообщить о том, что номер использован и отменить активацию
                        self.__close_fb_app(driver['driver'], profile_index)
                        self.__after_closing(profile_index)
                        driver['driver'] = self.__proxy_check(driver['driver'], driver['caps'])
                elif reg_status == 0:
                    driver['driver'] = self.__unsuc_reg(driver['driver'], sms_activate, profile_index, driver['caps'])
                elif reg_status == -1:
                    break
            except Exception as exc:
                print('Failed. ' + str(exc))
                driver['driver'] = self.__unsuc_reg(driver['driver'], sms_activate, profile_index, driver['caps'])
                continue

    @pyqtSlot()
    def run(self):
        self.ld_console.set_path(self.__path_to_ldplayer)
        sms_activate = SMSActivateAPI(self.__smsactivate_api_key)
        sms_activate.debug_mode = True  # TEMP?

        prof_data = self.__get_profile_data()
        emails = self.__get_emails()
        if emails is None:
            self.signals.finished.emit()
            return

        self.__title = RandomGenerator.random_username(8)  # рвндомное название плеера
        self.ld_console.add(self.__title)  # создаем плеер

        n_cord, e_cord = self.random_coord_generator.get_rand_coord(self.__geo)

        profile_index = self.ld_console.get_profile_index(self.__title)
        line = self.ld_console.find_num_of_line(profile_index)
        self.ld_console.set_debug_mode(profile_index, line)
        self.ld_console.set_location(profile_index, line, cord_n=n_cord, cord_e=e_cord)

        number = RandomNumGenerator.get_rand_mob_num()
        self.ld_console.modify(self.__title, str(number))
        self.ld_console.launch(self.__title)
        time.sleep(10)  # TEMP

        device = self.__get_device(profile_index)
        caps = {"platformName": "Android", "udid": str(AdbManager.get_dict_value_by_key(profile_index)),
                "newCommandTimeout": 99999}

        driver = self.__get_driver(3, caps)
        if not driver:
            self.__terminate(driver, device, profile_index)
            self.signals.finished.emit()
            return

        print("Profile " + str(self.__title) + " has been connected to Appium")
        self.signals.connected.emit()

        if self.__use_proxy:
            self.ld_console.install_app(self.__title, app_name=r'apps\drony.apk')
            driver = self.__init_drony(driver, caps, profile_index)

        driver = {"driver": driver, "caps": caps}
        self.ld_console.install_app(self.__title, app_name=r'apps\facebook_lite_v348.0.0.8.103.apk')

        self.__loop(driver, sms_activate, prof_data, emails, profile_index)

        self.__exit(self.ld_console, driver['driver'], self.__title)
        AdbManager.delete_index_from_dict(profile_index)
        AdbManager.remove_launched_device(device)
        self.signals.finished.emit()
