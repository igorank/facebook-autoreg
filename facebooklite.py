import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains, ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.mobileby import MobileBy


def find_element(driver, find_by, element, alternative_element=None,
                 alternative_element2=None, alternative_element3=None):
    for _ in range(15):
        try:
            time.sleep(3)
            if find_by == "id":
                return driver.find_element(MobileBy.ID, str(element))
            if find_by == "ac_id":
                return driver.find_element(MobileBy.ACCESSIBILITY_ID, str(element))
            if find_by == "xpath":
                return driver.find_element(MobileBy.XPATH, str(element))
        except NoSuchElementException:
            if alternative_element is not None:
                try:
                    if find_by == "id":
                        return driver.find_element(MobileBy.ID, str(alternative_element))
                    if find_by == "ac_id":
                        return driver.find_element(MobileBy.ACCESSIBILITY_ID, str(alternative_element))
                    if find_by == "xpath":
                        return driver.find_element(MobileBy.XPATH, str(alternative_element))
                except NoSuchElementException:
                    if alternative_element2 is not None:
                        try:
                            if find_by == "id":
                                return driver.find_element(MobileBy.ID, str(alternative_element2))
                            if find_by == "ac_id":
                                return driver.find_element(MobileBy.ACCESSIBILITY_ID, str(alternative_element2))
                            if find_by == "xpath":
                                return driver.find_element(MobileBy.XPATH, str(alternative_element2))
                        except NoSuchElementException:
                            if alternative_element3 is not None:
                                try:
                                    if find_by == "id":
                                        return driver.find_element(MobileBy.ID, str(alternative_element3))
                                    if find_by == "ac_id":
                                        return driver.find_element(MobileBy.ACCESSIBILITY_ID,
                                                                   str(alternative_element3))
                                    if find_by == "xpath":
                                        return driver.find_element(MobileBy.XPATH, str(alternative_element3))
                                except NoSuchElementException:
                                    pass
        time.sleep(2)
    print(str(element) + " can not be found")
    time.sleep(9999)  # TEMP
    # raise ValueError(str(element) + " can not be found")


class FacebookLite:

    def __init__(self, driver, phone):
        self.driver = driver
        self.phone = phone
        self.find_element = find_element

    def __check_fb_loaded(self) -> bool:
        try:
            WebDriverWait(self.driver, 25).until(
                EC.visibility_of_element_located(
                    (MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button')))
            return True
        except Exception:
            print("Failed to initialize Facebook Lite. Check Internet connection")
            return False

    def __fill_reg_form1(self, name):
        self.find_element(self.driver, "xpath",  # Создать акк
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.View",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup[3]",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup[3]").click()
        self.find_element(self.driver, "xpath",  # Далее
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup[1]",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.view.ViewGroup[1]").click()
        self.find_element(self.driver, "xpath",  # Имя
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView[1]",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView[1]",
                          "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView[1]").send_keys(
            name)

    def __enter_surname(self, surname):
        while True:
            try:
                self.driver.find_element(MobileBy.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView[2]').send_keys(
                    surname)
                break
            except NoSuchElementException:
                try:
                    self.driver.find_element(MobileBy.XPATH,
                                             '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView[2]').send_keys(
                        surname)
                    break
                except NoSuchElementException:
                    continue

    def __click_next(self):
        while True:
            try:
                self.driver.find_element(MobileBy.XPATH,  # Далее
                                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.view.ViewGroup[1]").click()
                break
            except NoSuchElementException:
                try:
                    self.driver.find_element(MobileBy.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup[1]").click()
                    break
                except NoSuchElementException:
                    continue

    def __enter_email(self, email):
        find_element(self.driver, "xpath",  # Зарегис. с эл. адресом
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[6]/android.view.ViewGroup[2]/android.view.View",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[6]/android.view.ViewGroup[2]/android.view.View").click()  # зарег с помощью почты кнопка
        find_element(self.driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView").send_keys(
            email)  # email field
        find_element(self.driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup[1]").click()  # Next Button

    def __enter_phone_num(self):
        find_element(self.driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView").send_keys(
            self.phone)  # phone number
        find_element(self.driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]").click()  # next button

    def __click_next2(self):
        find_element(self.driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup[2]",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[2]").click()  # next

    def __choose_gender(self):
        WebDriverWait(self.driver, 40).until(EC.any_of(
            EC.element_to_be_clickable((MobileBy.XPATH,
                                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.View[1]")),
            EC.element_to_be_clickable((MobileBy.XPATH,
                                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.View[1]"))
        ))
        find_element(self.driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.View[1]",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.View[1]").click()  # female text

    def __finishing_registration(self):
        find_element(self.driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.view.ViewGroup[1]",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup[1]").click()  # next
        find_element(self.driver, "xpath",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.view.ViewGroup[7]",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup[7]",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[5]",
                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[5]").click()

    def __date_field_available(self):
        for _ in range(10):
            try:
                if self.driver.find_element(MobileBy.XPATH,
                                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup[1]"):
                    return True
            except NoSuchElementException:
                try:
                    if self.driver.find_element(MobileBy.XPATH,
                                                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[1]"):
                        return True
                except NoSuchElementException:
                    pass
            time.sleep(2)
        print("Error: can't find date field")
        return False

    def __send_year_facebooklite(self):
        while True:
            try:
                self.driver.find_element(MobileBy.XPATH,
                                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[4]/android.view.ViewGroup[1]/android.view.View").click()  # 1
                break
            except NoSuchElementException:
                try:
                    self.driver.find_element(MobileBy.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[3]/android.view.ViewGroup[1]/android.view.View").click()  # 1
                    break
                except NoSuchElementException:
                    continue
        time.sleep(0.5)
        while True:
            try:
                self.driver.find_element(MobileBy.XPATH,
                                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[4]/android.view.ViewGroup[9]/android.view.View").click()  # 9
                break
            except NoSuchElementException:
                try:
                    self.driver.find_element(MobileBy.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[3]/android.view.ViewGroup[9]/android.view.View").click()  # 9
                    break
                except NoSuchElementException:
                    continue
        time.sleep(0.5)
        while True:
            try:
                self.driver.find_element(MobileBy.XPATH,
                                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[4]/android.view.ViewGroup[9]/android.view.View").click()  # 9
                break
            except NoSuchElementException:
                try:
                    self.driver.find_element(MobileBy.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[3]/android.view.ViewGroup[9]/android.view.View").click()  # 9
                    break
                except NoSuchElementException:
                    continue
        time.sleep(0.5)
        num1 = random.randint(1, 9)
        while True:
            try:
                self.driver.find_element(MobileBy.XPATH,
                                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[4]/android.view.ViewGroup[" + str(
                                             num1) + "]/android.view.View").click()
                # random
                break
            except NoSuchElementException:
                try:
                    self.driver.find_element(MobileBy.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[3]/android.view.ViewGroup[" + str(
                                                 num1) + "]/android.view.View").click()  # random
                    break
                except NoSuchElementException:
                    continue
        return str("199") + str(num1)

    def __send_day_facebooklite(self) -> str:
        time.sleep(0.5)
        num1 = random.randint(1, 2)
        while True:
            try:
                self.driver.find_element(MobileBy.XPATH,
                                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[4]/android.view.ViewGroup[" + str(
                                             num1) + "]/android.view.View").click()  # random 1-2
                break
            except NoSuchElementException:
                try:
                    self.driver.find_element(MobileBy.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[3]/android.view.ViewGroup[" + str(
                                                 num1) + "]/android.view.View").click()  # random 1-2
                    break
                except NoSuchElementException:
                    continue
        time.sleep(0.5)
        num2 = random.randint(1, 8)
        while True:
            try:
                self.driver.find_element(MobileBy.XPATH,
                                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[4]/android.view.ViewGroup[" + str(
                                             num2) + "]/android.view.View").click()  # random 1-8
                break
            except NoSuchElementException:
                try:
                    self.driver.find_element(MobileBy.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[3]/android.view.ViewGroup[" + str(
                                                 num2) + "]/android.view.View").click()  # random 1-8
                    break
                except NoSuchElementException:
                    continue
        return str(num1) + str(num2)

    def __send_month_facebooklite(self):
        time.sleep(0.5)
        while True:
            try:
                self.driver.find_element(MobileBy.XPATH,
                                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[4]/android.view.ViewGroup[11]/android.view.View").click()  # 0
                break
            except NoSuchElementException:
                try:
                    self.driver.find_element(MobileBy.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[3]/android.view.ViewGroup[11]/android.view.View").click()  # 0
                    break
                except NoSuchElementException:
                    continue
        time.sleep(0.5)
        num1 = random.randint(1, 8)
        while True:
            try:
                self.driver.find_element(MobileBy.XPATH,
                                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[4]/android.view.ViewGroup[" + str(
                                             num1) + "]/android.view.View").click()  # random 1-8
                break
            except NoSuchElementException:
                try:
                    self.driver.find_element(MobileBy.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[3]/android.view.ViewGroup[" + str(
                                                 num1) + "]/android.view.View").click()  # random 1-8
                    break
                except NoSuchElementException:
                    continue
        return str(0) + str(num1)

    def __password_field_available(self):
        for _ in range(30):
            try:
                if self.driver.find_element(MobileBy.XPATH,
                                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView"):
                    return True
            except NoSuchElementException:
                try:
                    if self.driver.find_element(MobileBy.XPATH,
                                                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView"):
                        return True
                except NoSuchElementException:
                    pass
            time.sleep(2)
        print("Error: can't find password field")
        return False

    @staticmethod
    def __delay_send(actions, word, delay):
        for i in word:
            actions.send_keys(i)
            actions.perform()
            time.sleep(delay)

    def __check_checkpoint_lite(self) -> int:
        for _ in range(30):
            try:
                if self.driver.find_element(MobileBy.XPATH,
                                            "//android.view.View[@content-desc=\"Скачать информацию\"]/android.widget.TextView"):
                    print("Checkpoint")
                    return 1
            except NoSuchElementException:
                try:
                    if self.driver.find_element(MobileBy.XPATH,
                                                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]"):
                        print("Checkpoint")
                        return 1
                except NoSuchElementException:
                    try:
                        if self.driver.find_element(MobileBy.XPATH,
                                                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView"):
                            print("Email has been already used")
                            return 1
                    except NoSuchElementException:
                        try:
                            if self.driver.find_element(MobileBy.XPATH,
                                                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.View[5]"):
                                print("Unknown error")
                                return 1
                        except NoSuchElementException:
                            try:
                                self.driver.find_element(MobileBy.XPATH,
                                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.View').click()
                                print("Successful registration")
                                find_element(self.driver, "id",
                                             "com.android.packageinstaller:id/permission_deny_button").click()
                                return 0
                            except NoSuchElementException:
                                try:
                                    self.driver.find_element(MobileBy.XPATH,
                                                             '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.View').click()
                                    print("Successful registration")
                                    find_element(self.driver, "id",
                                                 "com.android.packageinstaller:id/permission_deny_button").click()
                                    return 0
                                except NoSuchElementException:
                                    try:
                                        self.driver.find_element(MobileBy.XPATH,
                                                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.View[3]').click()  # "произошла ошибка"
                                        find_element(self.driver, "xpath",
                                                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[7]",
                                                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[7]",
                                                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[5]",
                                                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[5]").click()  # registration
                                    except NoSuchElementException:
                                        try:
                                            self.driver.find_element(MobileBy.XPATH,
                                                                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.View")
                                            print("Redirection error")
                                            return 1
                                        except NoSuchElementException:
                                            try:
                                                self.driver.find_element(MobileBy.XPATH,
                                                                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.View")
                                                print("Redirection error")
                                                return 1
                                            except NoSuchElementException:
                                                pass
            time.sleep(3)
        print("Error")
        return 2

    def register(self, profile_data, num_or_email, use_email):
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))

        try:
            WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, 'Lite')))
            self.driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Lite').click()

            if not self.__check_fb_loaded():
                return 0

            self.driver.find_element(MobileBy.ID, 'com.android.packageinstaller:id/permission_deny_button').click()
            self.__fill_reg_form1(profile_data['name'])
            self.__enter_surname(profile_data['surname'])
            self.__click_next()

            for _ in range(3):
                self.find_element(self.driver, "id", "com.android.packageinstaller:id/permission_deny_button").click()

            if use_email:
                self.__enter_email(num_or_email)
            else:
                self.__enter_phone_num()

            if self.__date_field_available():
                day = self.__send_day_facebooklite()
                month = self.__send_month_facebooklite()
                year = self.__send_year_facebooklite()
                date_of_birth = day + "." + month + "." + year
            else:
                return 0

            self.__click_next2()  # next
            self.__choose_gender()

            if self.__password_field_available():
                time.sleep(1)
                self.__delay_send(actions, profile_data['password'], random.uniform(0.05, 0.1))
                time.sleep(1)
            else:
                return 0

            self.__finishing_registration()
        except NameError as name_error:
            print(name_error)
            return -1
        except ValueError as value_error:
            print(value_error)
            return 0
        if self.__check_checkpoint_lite() == 0:
            return date_of_birth
        return 0
