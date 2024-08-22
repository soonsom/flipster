from common.helper_functions import HelperFunctions
from common.xpath_converter import get_aid, get_xpath_contains, get_value, get_xpath_by_direct_value


class TradePage(HelperFunctions):
    @Screenshot()
    def go_to_trade(self):
        self.wait_and_click_element(get_aid("gnb_trade"))
        self.wait_for_element_present(get_aid("trade_tab_explore"))
