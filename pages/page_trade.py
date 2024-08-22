from common.helper_functions import HelperFunctions
from common.xpath_converter import get_aid, get_xpath_contains, get_value, get_xpath_by_direct_value


class TradePage(HelperFunctions):
    @Screenshot()
    def go_to_trade(self):
        self.wait_and_click_element(get_aid("gnb_trade"))
        self.wait_for_element_present(get_aid("trade_tab_explore"))

    @Screenshot()
    def verify_displays_trade(self):
        els = [
            "trade_tab_explore",
            "trade_tab_list",
            "trade_product_list_main_title",
            "trade_product_list_main_info_icon",
        ]
        return self.get_els_not_shown(els)
