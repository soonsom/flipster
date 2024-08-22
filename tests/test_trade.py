import pytest

from pages.page_trade import TradePage


class TestTrade:
    @pytest.mark.p1
    @pytest.mark.usefixtures("go_to_trade")
    def test_trade(self):
        soft_assertions = []
        els_not_shown = TradePage().verify_displays_trade()
        if els_not_shown:
            soft_assertions.append(f"The following elements are not shown, {els_not_shown}")
