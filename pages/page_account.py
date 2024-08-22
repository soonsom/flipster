import os
from time import sleep

from selenium.common import TimeoutException

from common.helper_functions import HelperFunctions
from common.xpath_converter import get_aid, get_xpath_by_name, get_xpath_by_direct_value
from utils.enums import Selector, XpathType
from utils.screenshot import Screenshot


class AccountPage(HelperFunctions):
    @Screenshot()
    def go_to_account(self):
        self.wait_and_click_element(get_aid("menu_icon"))
        self.wait_for_element_present(get_aid("account_main_title"))

    def get_nickname(self):
        aid_nickname = get_aid("account_nick_value_01")
        self.wait_for_element_present(aid_nickname)
        return self.get_element_text(aid_nickname)

    def go_to_auth_settings(self):
        self.small_scroll_down()
        self.wait_and_click_element(get_xpath_by_name("account_auth_settings",
                                                      ios_attr_type="label"),
                                    find_by=Selector.XPATH)

        # android에서 webview element 식별이 느린 타이밍 이슈가 있어 sleep
        if os.environ["PLATFORM"] == "android":
            sleep(2)

        self.wait_for_element_present(get_xpath_by_name("account_auth", ios_attr_type="label"), find_by=Selector.XPATH)

    def verify_nickname(self, nickname):
        return self.is_element_present(get_xpath_by_direct_value(nickname),
                                       find_by=Selector.XPATH)

    def get_email_els_not_shown(self):
        email_account = os.environ["ID"][0:2]
        # android에서 email 영역 element가 내려오는 시간이 늦은경우가 있어 로드할때까지 wait
        email_els = [email_account,
                     "@",
                     ".com"]
        return self.get_els_not_shown(email_els, xpath_type=XpathType.DIRECT_VALUE)
