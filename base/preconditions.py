from common import values
from pages.page_preconditions import PreconditionPage


class Preconditions:
    def setup_permissions(self):
        PreconditionPage().permission_do_not_allow()

    def close_main_botton_sheet(self):
        PreconditionPage().close_main_bottom_sheet()

    def set_gnb_y(self):
        values.gnb_y = PreconditionPage().get_gnb_y()
