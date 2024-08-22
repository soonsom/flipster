from common import values
from common.helper_functions import HelperFunctions
from common.xpath_converter import get_aid, get_xpath_by_name


class AssetsPage(HelperFunctions):
    def go_to_assets(self):
        self.wait_and_click_element(get_aid("gnb_assets"))

        if values.is_logged_in:
            self.wait_for_element_present(get_aid("assets_verify_identity_img"))
        else:
            self.wait_for_element_present(get_aid("login_main_tit"))
