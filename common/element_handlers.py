import os

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from base import app
from common import values
from common.xpath_converter import get_xpath_by_direct_value
from utils.enums import Selector

TIMEOUT_5_SEC = 5


class ElementHandler(object):
    def is_element_present(self,
                           value,
                           find_by=Selector.AID):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        try:
            app.driver.find_element(selector, value)
        except NoSuchElementException:
            return False

        return True

    def wait_for_element_present(self, value, find_by=Selector.AID, timeout=TIMEOUT_5_SEC):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        try:
            WebDriverWait(app.driver, timeout).until(EC.presence_of_element_located((selector, value)))
        except TimeoutException as e:
            raise TimeoutException(f"No such element, {find_by}: {value} \n\n [Error] {str(e)}")

    def wait_for_element_not_present(self, value, find_by=Selector.AID, timeout=TIMEOUT_5_SEC):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        try:
            WebDriverWait(app.driver, timeout).until(EC.invisibility_of_element_located((selector, value)))
        except TimeoutException as e:
            raise TimeoutException(f"Element still shown, {find_by}: {value} \n\n [Error] {str(e)}")

    def wait_and_click_element(self, value, find_by=Selector.AID, timeout=TIMEOUT_5_SEC):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        try:
            WebDriverWait(app.driver, timeout).until(EC.element_to_be_clickable((selector, value))).click()
        except TimeoutException as e:
            raise TimeoutException(f"No such element to click, {find_by}: {value} \n\n [Error] {str(e)}")

    def click_element(self, value, find_by=Selector.AID):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        try:
            app.driver.find_element(selector, value).click()
        except Exception as e:
            raise Exception(f"No such element to click, {find_by}: {value} \n\n [Error] {str(e)}")

    # **kwargs: textfied, value
    # the name of key should be textfield or value
    def input_text_by_find_by(self, find_by=Selector.AID, **kwargs):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        textfields = []
        values = []
        for key, value in kwargs.items():
            if "textfield" in key:
                textfields.append(value)
            elif "value" in key:
                values.append(value)

        for index, field in enumerate(textfields):
            try:
                textfield = app.driver.find_element(selector, field)
                textfield.click()
            except Exception as e:
                raise Exception(f"No such element, {find_by}: {value} \n\n [Error] {str(e)}")
            try:
                textfield.send_keys(values[index])
            except Exception as e:
                raise Exception(f"Unable to send keys to the text field, {find_by}: {value} \n\n [Error] {str(e)}")

    def get_element(self, value, find_by=Selector.AID):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        try:
            el = app.driver.find_element(selector, value)
        except NoSuchElementException as e:
            raise NoSuchElementException(f"No such element, {find_by}: {value} \n\n [Error] {str(e)}")

        return el

    def get_elements(self, value, find_by=Selector.AID):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        try:
            els = app.driver.find_elements(selector, value)
        except NoSuchElementException as e:
            raise NoSuchElementException(f"No such elements, {find_by}: {value} \n\n [Error] {str(e)}")

        return els

    def get_child_element(self, parent_el, value, find_by=Selector.AID):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        try:
            el = parent_el.find_element(selector, value)
        except NoSuchElementException as e:
            raise NoSuchElementException(f"No such child element, {find_by}: {value} \n\n [Error] {str(e)}")

        return el

    def get_element_text(self, value, find_by=Selector.AID):
        el = self.get_element(value, find_by=find_by)
        return el.text

    def hide_keyboard(self):
        if os.environ["PLATFORM"] == "android":
            app.driver.hide_keyboard()
        else:
            self.wait_and_click_element(get_xpath_by_direct_value("done"), find_by=Selector.XPATH, timeout=3)

    def get_element_location(self, value, find_by=Selector.AID):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        try:
            el = app.driver.find_element(selector, value)
        except NoSuchElementException as e:
            raise NoSuchElementException(f"No such element, {find_by}: {value} \n\n [Error] {str(e)}")

        return el.location

    def get_element_size(self, value, find_by=Selector.AID):
        selector = By.XPATH if find_by == Selector.XPATH else MobileBy.ACCESSIBILITY_ID
        try:
            el = app.driver.find_element(selector, value)
        except NoSuchElementException as e:
            raise NoSuchElementException(f"No such child element, {find_by}: {value} \n\n [Error] {str(e)}")

        return el.size

    def get_app_size(self):
        app_xpath = {
            "ios": "//XCUIElementTypeApplication",
            "android": "/hierarchy/android.widget.FrameLayout"
        }
        return self.get_element_size(app_xpath[os.environ["PLATFORM"]], find_by=Selector.XPATH)

    def tap_by_coordinate(self, x, y):
        TouchAction(app.driver).tap(x=x, y=y).perform()

    def scroll_by_coordinate(self,
                             start_y,
                             end_y, x=100,
                             wait_until=0):
        if os.environ["PLATFORM"] == "ios":
            TouchAction(app.driver).\
                long_press(None, x, start_y)\
                .wait(wait_until * 1000)\
                .move_to(None, x, end_y)\
                .release()\
                .perform()
        else:
            app.driver.swipe(x, start_y, x, end_y)

    def regular_scroll_down(self):
        start_y = values.gnb_y-10
        end_y = self.get_app_size()["height"]/2

        self.scroll_by_coordinate(start_y=start_y, end_y=end_y)

    def small_scroll_down(self):
        minus = {
            "ios": 50,
            "android": 10
        }
        divide = {
            "ios": 1.5,
            "android": 1.3
        }
        start_y = values.gnb_y-minus[os.environ["PLATFORM"]]
        end_y = self.get_app_size()["height"]/divide[os.environ["PLATFORM"]]

        self.scroll_by_coordinate(start_y=start_y, end_y=end_y)

    def swipe_to_left_on_element(self,
                                 xpath,
                                 find_by=Selector.AID,
                                 start_x=None,
                                 end_x=None):
        el_height = self.get_element_size(xpath, find_by=find_by)["height"]
        el_y = self.get_element_location(xpath, find_by=find_by)["y"]
        y = el_y + el_height/2
        divide = {
            "ios": 5,
            "android": 2
        }
        if start_x is None:
            start_x = self.get_app_size()["width"]/divide[os.environ["PLATFORM"]]
        if end_x is None:
            end_x = 10

        app.driver.swipe(start_x=start_x, end_x=end_x, start_y=y, end_y=y)
