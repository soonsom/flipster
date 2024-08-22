import pytest

from common.helper_functions import HelperFunctions
from pages.page_assets import AssetsPage


class TestAssets(HelperFunctions):
    @pytest.mark.p1
    @pytest.mark.usefixtures("go_to_assets")
    def test_assets_login(self):
        soft_assertion = AssetsPage().verify_displays_login()
        AssetsPage().login()

        # 디스플레이 체크 오류가 있는 경우 AssertionError 발생
        if soft_assertion:
            raise AssertionError(f"[login] The following elements are not shown, {soft_assertion}")

    @pytest.mark.p1
    @pytest.mark.usefixtures("go_to_assets")
    def test_assets_main(self):
        soft_assertions = []
        AssetsPage().regular_scroll_down()

        els_not_shown = AssetsPage().verify_displays_assets()
        if els_not_shown:
            soft_assertions.append(f"The following elements are not shown: {els_not_shown} \n")
