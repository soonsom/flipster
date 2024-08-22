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
