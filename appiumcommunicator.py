import time
import random
from appium.webdriver.common.mobileby import MobileBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

class AppiumCommunicator:

    @staticmethod
    def find_element(driver, find_by, element, alternative_element=None, alternative_element2=None, alternative_element3=None):
        it = 0
        while it < 15:
            try:
                if driver.find_element(MobileBy.ID, 'android:id/aerr_close'):
                    print("The application LD Store crashed")
                    raise NameError("The application LD Store crashed")
            except:
                pass
            try:
                # print("Looking for " + str(element) + " element")
                time.sleep(3)
                if find_by == "id":
                    return driver.find_element(MobileBy.ID, str(element))
                    # return driver.find_element_by_id(str(element))
                elif find_by == "ac_id":
                    return driver.find_element(MobileBy.ACCESSIBILITY_ID, str(element))
                    # return driver.find_element_by_accessibility_id(str(element))
                elif find_by == "xpath":
                    return driver.find_element(MobileBy.XPATH, str(element))
                    # return driver.find_element_by_xpath(str(element))
            except:
                if alternative_element is not None:
                    try:
                        # print("Looking for " + str(alternative_element) + " element")
                        if find_by == "id":
                            return driver.find_element(MobileBy.ID, str(alternative_element))
                            # return driver.find_element_by_id(str(alternative_element))
                        elif find_by == "ac_id":
                            return driver.find_element(MobileBy.ACCESSIBILITY_ID, str(alternative_element))
                            # return driver.find_element_by_accessibility_id(str(alternative_element))
                        elif find_by == "xpath":
                            return driver.find_element(MobileBy.XPATH, str(alternative_element))
                            # return driver.find_element_by_xpath(str(alternative_element))
                    except:
                        if alternative_element2 is not None:
                            try:
                                if find_by == "id":
                                    return driver.find_element(MobileBy.ID, str(alternative_element2))
                                    # return driver.find_element_by_id(str(alternative_element2))
                                elif find_by == "ac_id":
                                    return driver.find_element(MobileBy.ACCESSIBILITY_ID, str(alternative_element2))
                                    # return driver.find_element_by_accessibility_id(str(alternative_element2))
                                elif find_by == "xpath":
                                    return driver.find_element(MobileBy.XPATH, str(alternative_element2))
                                    # return driver.find_element_by_xpath(str(alternative_element2))
                            except:
                                if alternative_element3 is not None:
                                    try:
                                        if find_by == "id":
                                            return driver.find_element(MobileBy.ID, str(alternative_element3))
                                            # return driver.find_element_by_id(str(alternative_element3))
                                        elif find_by == "ac_id":
                                            return driver.find_element(MobileBy.ACCESSIBILITY_ID,
                                                                       str(alternative_element3))
                                            # return driver.find_element_by_accessibility_id(str(alternative_element3))
                                        elif find_by == "xpath":
                                            return driver.find_element(MobileBy.XPATH, str(alternative_element3))
                                            # return driver.find_element_by_xpath(str(alternative_element3))
                                    except:
                                        pass
                                pass
                        pass
            time.sleep(2)
            it += 1
        raise ValueError(str(element) + " can not be found")

    @staticmethod
    def check_drony_loaded(driver):
        status = 0
        while status == 0:
            try:
                if driver.find_element_by_id("org.sandrob.drony:id/toggleButtonOnOff"):
                    return 0
            except:
                time.sleep(2)

    @staticmethod
    def check_right_swap_drony(driver):
        while True:
            if driver.find_element_by_xpath(
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[8]/android.widget.RelativeLayout"):
                return 0
            else:
                time.sleep(3)

    @staticmethod
    def check_left_swap_drony(driver):
        while True:
            if driver.find_element(MobileBy.ID, "org.sandrob.drony:id/toggleButtonOnOff"):
                return 0
            else:
                time.sleep(3)

    @staticmethod
    def fb_lite_loaded(driver):
        it = 0
        while it < 15:
            try:
                if driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button"):
                    return True
            except:
                it += 1
                time.sleep(1)
        return False

    @staticmethod
    def swipe_right(actions):
        actions.w3c_actions.pointer_action.move_to_location(522, 480)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(17, 475)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    @staticmethod
    def swipe_left(actions):
        actions.w3c_actions.pointer_action.move_to_location(11, 529)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(522, 534)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    @staticmethod
    def swipe_down(actions):
        actions.w3c_actions.pointer_action.move_to_location(264, 791)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(268, 630)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    @staticmethod
    def tap_by_cordinates(actions, x, y):
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    @staticmethod
    def delay_send(actions, word, delay):
        for c in word:
            actions.send_keys(c)
            actions.perform()
            time.sleep(delay)

    @staticmethod
    def password_field_available(driver):
        it = 0
        while it < 30:
            try:
                if driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView"):
                    return True
            except:
                try:
                    if driver.find_element_by_xpath(
                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.widget.MultiAutoCompleteTextView"):
                        return True
                except:
                    pass
                pass
            time.sleep(2)
            it += 1
        print("Error: can't find password field")
        return False

    @staticmethod
    def date_field_available(driver):
        it = 0
        while it < 10:
            try:
                if driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup[1]"):
                    return True
            except:
                try:
                    if driver.find_element_by_xpath(
                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[1]"):
                        return True
                except:
                    pass
                pass
            time.sleep(2)
            it += 1
        print("Error: can't find date field")
        return False

    @staticmethod
    def check_checkpoint_lite(driver):
        it = 0
        while it < 30:
            try:
                if driver.find_element_by_xpath(
                        "//android.view.View[@content-desc=\"Скачать информацию\"]/android.widget.TextView"):
                    print("Checkpoint")
                    return 1
            except:
                try:
                    if driver.find_element_by_xpath(
                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]"):
                        print("Checkpoint")
                        return 1
                except:
                    try:
                        if driver.find_element_by_xpath(
                                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.MultiAutoCompleteTextView"):
                            print("Email has been already used")
                            return 1
                    except:
                        try:
                            if driver.find_element_by_xpath(
                                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.View[5]"):
                                print("Unknown error")
                                return 1
                        except:
                            try:
                                # driver.find_element_by_xpath(
                                #     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.View").click()
                                driver.find_element(MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.View').click()
                                print("Successful registration")
                                AppiumCommunicator.find_element(driver, "id",
                                                                "com.android.packageinstaller:id/permission_deny_button").click()
                                return 0
                            except:
                                try:
                                    # driver.find_element_by_xpath(
                                    #     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.View").click()
                                    driver.find_element(MobileBy.XPATH,
                                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.View').click()
                                    print("Successful registration")
                                    AppiumCommunicator.find_element(driver, "id",
                                                                    "com.android.packageinstaller:id/permission_deny_button").click()
                                    return 0
                                except:
                                    try:
                                        driver.find_element(MobileBy.XPATH,
                                                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.View[3]').click()    #  "произошла ошибка"
                                        AppiumCommunicator.find_element(driver, "xpath",
                                                      "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[7]",
                                                      "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[7]",
                                                      "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[5]",
                                                      "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[5]").click()  # registration
                                    except:
                                        try:
                                            driver.find_element(MobileBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.View")
                                            print("Redirection error")
                                            return 1
                                        except:
                                            try:
                                                driver.find_element(MobileBy.XPATH,
                                                                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.View")
                                                print("Redirection error")
                                                return 1
                                            except:
                                                pass
                                            pass
                                        pass
                                    pass
                                pass
                            pass
                        pass
                    pass
                pass
            time.sleep(3)
            it += 1
        print("Error")
        return 2

    @staticmethod
    def check_registration(driver, use_email=False):
        it = 0
        while it < 45:
            if not use_email:
                try:
                    # BUG
                    if driver.find_element_by_xpath(
                            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[3]"):
                        print("Profile verified")
                        return True
                except:
                    pass
            else:
                pass
            try:
                if driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.View[2]"):
                    print("Profile verified")
                    return True
            except:
                pass
            try:
                if driver.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.View[2]"):
                    print("Profile verified")
                    return True
            except:
                pass
            try:
                driver.find_element(MobileBy.XPATH,
                                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.View[3]').click()  # "произошла ошибка"
                AppiumCommunicator.find_element(driver, "xpath",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]",
                                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]").click()
            except:
                pass
            time.sleep(2)
            it += 1
        print("Error. Profile has not been verified")
        return False

    @staticmethod
    def send_year_facebooklite(driver):
        while True:
            try:
                driver.find_element_by_xpath(
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup[1]/android.view.View").click()  # 1
                break
            except:
                try:
                    driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[4]/android.view.ViewGroup[1]/android.view.View").click()  # 1
                    break
                except:
                    continue
        time.sleep(0.5)
        while True:
            try:
                driver.find_element_by_xpath(
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup[9]/android.view.View").click()  # 9
                break
            except:
                try:
                    driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[4]/android.view.ViewGroup[9]/android.view.View").click()  # 9
                    break
                except:
                    continue
        time.sleep(0.5)
        while True:
            try:
                driver.find_element_by_xpath(
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup[9]/android.view.View").click()  # 9
                break
            except:
                try:
                    driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[4]/android.view.ViewGroup[9]/android.view.View").click()  # 9
                    break
                except:
                    continue
        time.sleep(0.5)
        num1 = random.randint(1, 8)
        while True:
            try:
                driver.find_element_by_xpath(
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup[" + str(
                        num1) + "]/android.view.View").click()  # random
                break
            except:
                try:
                    driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[4]/android.view.ViewGroup[" + str(
                            num1) + "]/android.view.View").click()  # random
                    break
                except:
                    continue
        return str("199") + str(num1)

    @staticmethod
    def send_day_facebooklite(driver):
        time.sleep(0.5)
        num1 = random.randint(1, 2)
        while True:
            try:
                driver.find_element_by_xpath(
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup[" + str(
                        num1) + "]/android.view.View").click()  # random 1-2
                break
            except:
                try:
                    driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[4]/android.view.ViewGroup[" + str(
                            num1) + "]/android.view.View").click()  # random 1-2
                    break
                except:
                    continue
        time.sleep(0.5)
        num2 = random.randint(1, 8)
        while True:
            try:
                driver.find_element_by_xpath(
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup[" + str(
                        num2) + "]/android.view.View").click()  # random 1-8
                break
            except:
                try:
                    driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[4]/android.view.ViewGroup[" + str(
                            num2) + "]/android.view.View").click()  # random 1-8
                    break
                except:
                    continue
        return str(num1) + str(num2)

    @staticmethod
    def send_month_facebooklite(driver):
        time.sleep(0.5)
        while True:
            try:
                driver.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup[11]/android.view.View").click()  # 0
                break
            except:
                try:
                    driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[4]/android.view.ViewGroup[11]/android.view.View").click()  # 0
                    break
                except:
                    continue
        time.sleep(0.5)
        num1 = random.randint(1, 8)
        while True:
            try:
                driver.find_element_by_xpath(
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[3]/android.view.ViewGroup[" + str(
                        num1) + "]/android.view.View").click()  # random 1-8
                break
            except:
                try:
                    driver.find_element_by_xpath(
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[4]/android.view.ViewGroup[" + str(
                            num1) + "]/android.view.View").click()  # random 1-8
                    break
                except:
                    continue
        return str(0) + str(num1)

    @staticmethod
    def close_chrome(driver):
        driver.terminate_app('com.android.chrome')
