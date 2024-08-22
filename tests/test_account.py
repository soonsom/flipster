import pytest

from pages.page_account import AccountPage


class TestAccount:
    @pytest.mark.p1
    @pytest.mark.usefixtures("go_to_account")
    def test_account(self):
        soft_assertions = []
        # 비밀번호 변경 페이지에서 닉네임이 정상 노출되는지 보기 위해 닉네임을 얻어옴
        # api 에서 회원 닉네임을 받아올 수 있는 경우 account 페이지 에서도 한번 더 확인 가능
        nickname = AccountPage().get_nickname()
        AccountPage().go_to_auth_settings()

        assert_nickname = AccountPage().verify_nickname(nickname)
        email_els_not_shown = AccountPage().get_email_els_not_shown()

        if not assert_nickname:
            soft_assertions.append(f"The nickname, {nickname} is not shown \n")

        if email_els_not_shown:
            soft_assertions.append(f"Email elements are not shown, {email_els_not_shown}")

        if soft_assertions:
            raise AssertionError(soft_assertions)
