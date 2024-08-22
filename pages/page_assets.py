import os

from selenium.common import NoSuchElementException

from common import values
from common.helper_functions import HelperFunctions
from common.xpath_converter import get_aid, get_xpath_by_name
from utils.enums import Selector, XpathType
from utils.screenshot import Screenshot


class AssetsPage(HelperFunctions):
    @Screenshot()
    def go_to_assets(self):
        self.wait_and_click_element(get_aid("gnb_assets"))

        if values.is_logged_in:
            self.wait_for_element_present(get_aid("assets_verify_identity_img"))
        else:
            self.wait_for_element_present(get_aid("login_main_tit"))

    @Screenshot()
    def verify_displays_login(self):
        assertions = []
        aid_els_to_chk = [
            "menu_icon",
            "gift_icon",
            "login_thumbnail",
            "login_tab_forgot_your_password",
            "login_tab_get_started"
        ]
        xpath_els_to_chk = [
            "login_txt_or",
            "login_btn_tit_google",
            "login_txt_sign_up",
        ]
        if os.environ["PLATFORM"] == "ios":
            aid_els_to_chk[0] = "menu_icon_sign_in"

        self.regular_scroll_down()

        aid_els_not_shown = self.get_els_not_shown(aid_els_to_chk)
        text_els_not_shown = self.get_els_not_shown(xpath_els_to_chk, xpath_type=XpathType.XPATH)

        if aid_els_not_shown:
            assertions.append(aid_els_not_shown)
        if text_els_not_shown:
            assertions.append(text_els_not_shown)

        return assertions

    @Screenshot()
    def type_credentials(self):
        if os.environ["PLATFORM"] == "android":
            email = False
            pw = False
            textfield_android = "//android.widget.EditText"
            els = self.get_elements(textfield_android, find_by=Selector.XPATH)
            for el in els:
                try:
                    email = self.get_child_element(el, get_aid("login_textfield_email"))
                    el.click()
                    el.send_keys(os.environ["ID"])
                except NoSuchElementException:
                    try:
                        pw = self.get_child_element(el, get_aid("login_textfield_pw"))
                        el.click()
                        el.send_keys(os.environ["PASSWORD"])
                    except NoSuchElementException:
                        pass
        else:
            email = self.get_element(get_xpath_by_name("login_textfield_email"), find_by=Selector.XPATH)
            pw = self.get_element(get_xpath_by_name("login_textfield_pw"), find_by=Selector.XPATH)
            email.click()
            email.send_keys(os.environ["ID"])
            pw.click()
            pw.send_keys(os.environ["PASSWORD"])

        if not email or not pw:
            raise NoSuchElementException("either email or pw textfield not shown")

    @Screenshot()
    def login(self):
        self.type_credentials()
        if os.environ["PLATFORM"] == "android":
            self.hide_keyboard()
        else:
            lo = self.get_element_location(get_aid("login_tab_forgot_your_password"))
            width = self.get_element_size(get_aid("login_tab_forgot_your_password"))["width"]
            self.scroll_by_coordinate(start_y=lo["y"], end_y=0)

        self.wait_and_click_element(get_aid("login_tab_sign_in"))
        self.wait_for_element_present(get_aid("assets_verify_identity_img"))
        values.is_logged_in = True
