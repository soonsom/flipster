from common.element_handlers import ElementHandler
from common.xpath_converter import get_xpath_by_name, get_aid
from utils.enums import Selector


class PreconditionPage(ElementHandler):
    def permission_do_not_allow(self):
        do_not_allow = get_xpath_by_name("permission_do_not_allow")
        self.wait_and_click_element(do_not_allow, find_by=Selector.XPATH)
        self.wait_for_element_not_present(do_not_allow)

    def close_main_bottom_sheet(self):
        cls_btn = get_aid("close_btn")
        self.wait_and_click_element(cls_btn)
        self.wait_for_element_not_present(cls_btn)

    def get_gnb_y(self):
        gnb_assets = get_aid("gnb_assets")
        self.wait_for_element_present(gnb_assets)
        return self.get_element_location(gnb_assets)["y"]
