import os

import pytest

from common.helper_functions import HelperFunctions
from pages.page_assets import AssetsPage
from utils.logger import log


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

        # api에서 balance, total value 얻어와서 수행하도록 변경 필요
        # self.get_balance()
        # self.get_total_value()
        balance = os.environ["BALANCE"]
        total_value = os.environ["TOTAL_VALUE"]

        # android에선 balance 표기 시, 소수점 2자리까지 표현하지만
        # iOS에선 정수만 표기하기 때문에 분기
        if os.environ["PLATFORM"] == "ios":
            balance = balance.split(".")[0]
            print(f"balance_to_chk: {type(balance)}, {balance}")
            log.info(f"balance_to_chk: {type(balance)}, {balance}")

        current_balance = AssetsPage().get_balance()
        print(f"get_balance: {type(current_balance)}, {current_balance}")
        log.info(f"get_balance: {type(current_balance)}, {current_balance}")
        current_total_value = AssetsPage().get_total_value()

        if balance != current_balance:
            soft_assertions.append(f"balance should be {balance}, not {current_balance} \n")

        if total_value != current_total_value:
            soft_assertions.append(f"total value should be {balance}, not {current_total_value} \n")

        if soft_assertions:
            raise AssertionError(soft_assertions)
