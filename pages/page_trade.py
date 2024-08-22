import os

from common.helper_functions import HelperFunctions
from common.xpath_converter import get_aid, get_xpath_contains, get_value, get_xpath_by_direct_value
from utils.enums import Selector, XpathType
from utils.screenshot import Screenshot


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

    def get_updated_sectioin_list(self, list, section_index):
        els = [raw_el.replace("no", "no"+str(section_index)) for raw_el in list]
        return els

    @Screenshot()
    def verify_displays_tit_area(self, section_index):
        raw_els = [
            "trade_carousel_no_title",
            "trade_carousel_no_see_all",
            "trade_carousel_no_description"
        ]
        els = self.get_updated_sectioin_list(raw_els, section_index)

        return self.get_els_not_shown(els)

    @Screenshot()
    def verify_trading_list(self, trading_list, section_index):
        raw_els = [
            "trade_carousel_no_image",
            "trade_carousel_no_ticker",
            "trade_carousel_no_price",
            "trade_carousel_no_fluctuation"
        ]
        # 엘러멘트 xpath를 참조할 키 값을 trade_carousel_no2_image 형태로 업데이트
        els = self.get_updated_sectioin_list(raw_els, section_index)

        els_not_shown = []
        for trading_symbol in trading_list:
            els_for_trading = [get_value(el)+trading_symbol for el in els]

            raw_els_not_shown = self.get_els_not_shown(els_for_trading, xpath_type=XpathType.DIRECT_AID)
            if raw_els_not_shown:
                self.swipe_to_left_on_element(xpath=get_xpath_contains(els[0],
                                                                       android_attr_type="content-desc"),
                                              find_by=Selector.XPATH)

                tmp_els_not_shown = self.get_els_not_shown(raw_els_not_shown, xpath_type=XpathType.DIRECT_AID)
                if tmp_els_not_shown:
                    els_not_shown.append(tmp_els_not_shown)

        return els_not_shown

    @Screenshot()
    def go_to_order_form(self, trading_symbol, section_index):
        self.wait_and_click_element(get_xpath_by_direct_value(f"carousel_no{section_index}_ticker_{trading_symbol}",
                                                              android_attr_type="content-desc"),
                                    find_by=Selector.XPATH)
        self.wait_for_element_present(f'{get_aid("trade_order_form")}{trading_symbol}')

    @Screenshot()
    def verify_displays_order_form(self):
        els = [
            "order_form",
            f"order_form_favorite_icon_unselected_{os.environ['PLATFORM']}",
            "order_form_price_",
            "order_form_tab_chart_funding_info",
            "order_form_chart_funding_rate",
            "order_form_chart_funding_time",
            "order_form_tab_order_form_chart",
            "order_form_tab_order_form_stats",
            f"order_form_chart_container_{os.environ['PLATFORM']}",
            "back_icon"
        ]
        els_not_shown = self.get_els_not_shown(els, xpath_type=XpathType.CONTAINS)
        return els_not_shown
