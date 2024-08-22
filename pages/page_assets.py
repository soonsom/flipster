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

    @Screenshot()
    def verify_displays_assets(self):
        aid_els_to_chk = [
            "assets_verify_identity_img",
            "assets_title_no1",
            "assets_title_no1_info_icon",
            "assets_tab_pnl_analysis",
            "assets_title_no1_value_no1",
            "assets_title_no1_value_no2",
            "assets_title_no2",
            "assets_title_no2_text_no1" ,
            "assets_tab_order_form_positions_open",
            "assets_tab_order_form_positions_pending",
            "assets_positions_open_description",
            "assets_tab_history_icon",
            "assets_title_no3",
            "assets_title_no3_text_no1",
            "assets_ya_info_icon",
            "assets_ya_value_no1",
            "assets_ya_value_no2",
            "assets_convert_to_usdt"
        ]

        return self.get_els_not_shown(aid_els_to_chk)

    def get_balance(self):
        return self.get_element(get_aid("assets_title_no1_value_no1")).text

    def get_total_value(self):
        return self.get_element(get_aid("assets_ya_value_no1")).text

    @Screenshot()
    def go_to_identity_verification(self):
        self.click_element(get_aid("assets_verify_identity_img"))
        self.wait_for_element_present(get_xpath_by_name("identity_verification_tit"),
                                      find_by=Selector.XPATH)

    @Screenshot()
    def verify_displays_identity_verification(self):
        str_els = [
            "identity_verification_tit",
            f"identity_verification_faq_guide_{os.environ['PLATFORM']}",
            "identity_verification_btn_faq",
            "identity_verification_badge_level1",
            "identity_verification_badge_level2",
            "identity_verification_badge_level3",
            "identity_verification_badge_level4",
            "identity_verification_txt_verified",
            "identity_verification_btn_verify",
            "identity_verification_tit_email",
            "identity_verification_tit_identity",
            "identity_verification_tit_residential_addr",
            "identity_verification_tit_funds",
            "identity_verification_btn_help",
            "identity_verification_guide1",
            "identity_verification_guide2",
            "identity_verification_guide3",
        ]
        raw_str_els_not_shown = self.get_els_not_shown(str_els,
                                                       ios_attr_type="label",
                                                       xpath_type=XpathType.CONTAINS)
        if raw_str_els_not_shown:
            self.regular_scroll_down()
            els_not_shown = self.get_els_not_shown(raw_str_els_not_shown, xpath_type=XpathType.CONTAINS)
        else:
            els_not_shown = raw_str_els_not_shown

        return els_not_shown

    @Screenshot()
    def go_to_identity_complete_verification(self):
        self.wait_and_click_element(get_xpath_by_name("identity_verification_btn_verify",
                                                      ios_attr_type="label"),
                                    find_by=Selector.XPATH)
        self.wait_for_element_present(get_xpath_by_name("complete_verification_tit",
                                                        ios_attr_type="label"),
                                      find_by=Selector.XPATH,
                                      timeout=10)

    @Screenshot()
    def verify_displays_identity_complete_verification(self):
        label_els = [
            "complete_verification_tit",
            "complete_verification_sub_tit",
            "complete_verification_tit_profile",
            f"complete_verification_sub_tit_profile_{os.environ['PLATFORM']}",
            "complete_verification_tit_selfie",
            "complete_verification_sub_tit_selfie",
            "complete_verification_tit_id",
            "complete_verification_sub_tit_id",
            f"btn_continue",
        ]
        els_not_shown = []

        label_els_not_shown = self.get_els_not_shown(label_els,
                                                     ios_attr_type="label",
                                                     xpath_type=XpathType.XPATH)

        if label_els_not_shown:
            els_not_shown.append(label_els_not_shown)

        if os.environ["PLATFORM"] == "android":
            resource_id_els = [
                f"complete_verification_btn_cls_android",
                f"complete_verification_footer_android",
                "complete_verification_rights_android",
            ]
            resource_id_els_not_shown = self.get_els_not_shown(resource_id_els,
                                                               ios_attr_type="label",
                                                               android_attr_type="resource-id",
                                                               xpath_type=XpathType.XPATH)
            if resource_id_els_not_shown:
                els_not_shown.append(resource_id_els_not_shown)
        else:
            aid_els = [
                f"common_close_btn_ios",
                f"complete_verification_footer_ios",
            ]
            aid_els_not_shown = self.get_els_not_shown(aid_els,
                                                       xpath_type=XpathType.AID)
            if aid_els_not_shown:
                els_not_shown.append(aid_els_not_shown)

        return els_not_shown
