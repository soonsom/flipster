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

        # new listing 영역의 트레이딩 목록 확인
        # api로 리스트 값을 가져와서 위의 키 값들에 api에서 얻어온 trading 기업명을 연결해서 체크 필요
        # new_listing = self.get_api_trading_list(section="new_listing")
        new_listing = ["brett", "voxel", "sys", "g"]
        new_listing_not_shown = TradePage().verify_trading_list(trading_list=new_listing,
                                                                section_index=2)
        if new_listing_not_shown:
            soft_assertions.append(f"[new_listing] {new_listing_not_shown}")
