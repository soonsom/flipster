import os

from common.helper_functions import HelperFunctions
from common.xpath_converter import get_aid, get_xpath_by_name, get_xpath_by_direct_value
from utils.screenshot import Screenshot


class AccountPage(HelperFunctions):
    @Screenshot()
    def go_to_account(self):
        self.wait_and_click_element(get_aid("menu_icon"))
        self.wait_for_element_present(get_aid("account_main_title"))
