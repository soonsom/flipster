import pytest

from pages.page_trade import TradePage


class TestTrade:
    @pytest.mark.p1
    @pytest.mark.usefixtures("go_to_trade")
    def test_trade(self):
        soft_assertions = []

        # 상단 타이틀 영역 디스플레이 체크
        els_not_shown = TradePage().verify_displays_trade()
        if els_not_shown:
            soft_assertions.append(f"The following elements are not shown, {els_not_shown}")

        # new listing 타이틀 영역 디스플레이 체크
        TradePage().verify_displays_tit_area(section_index=2)
