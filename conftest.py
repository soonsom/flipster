import datetime
import os
import time

import pytest
from dotenv import load_dotenv
from selenium.common import TimeoutException

from base import app
from base.preconditions import Preconditions
from cleanup import update_logfile_to_device_name
from common import values
from pages.page_assets import AssetsPage
from pages.page_trade import TradePage
from utils.logger import log

from utils.html_report.html_report_customize import pytest_runtest_makereport

##### pytest html report (DO NOT REMOVE for generating a html report) #####
from utils.html_report.html_report_customize import pytest_html_report_title
from utils.html_report.html_report_customize import pytest_html_results_table_header
from utils.html_report.html_report_customize import pytest_html_results_table_row
from utils.html_report.html_report_customize import pytest_html_results_table_html
from utils.html_report.html_report_customize import pytest_html_results_summary
from utils.html_report.html_report_customize import pytest_sessionfinish

###############################

tests_count = 0


def pytest_addoption(parser):
    parser.addoption("--device", action="store", default="galaxys23")


def pytest_runtestloop(session):
    # 테스트 전반에 env 파일의 환경변수를 사용하기 위해 테스트 시작 시점에 load
    load_dotenv(os.path.abspath(f'./testinfo-{session.config.getoption("device")}.env'))


@pytest.mark.trylast
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    global tests_count

    platform = os.environ['PLATFORM']
    device = os.environ['DEVICE']
    platform_version = os.environ["OS_VERSION"]
    result_count_summary = ""

    duration = time.time() - terminalreporter._sessionstarttime
    duration_format = str(datetime.timedelta(seconds=round(duration)))

    summary = f"{result_count_summary[:-2]} / total: {tests_count} in ({duration_format})"
    log.info(f"[report][summary]: {summary}")

    # html report 파일명 변경
    old_file_name = os.path.abspath(f"./results/{os.environ['PLATFORM']}/report-{device}.html")
    new_file_name = os.path.abspath(
        f"./results/{os.environ['PLATFORM']}/TestReport_{platform}{platform_version}_{device}.html")

    log.debug(f"is_file: {os.path.isfile(old_file_name)}")

    try:
        os.rename(old_file_name, new_file_name)

        # slack html 파일 업로드 링크를 testrail에도 보내기 위해 변수 저장
    except (FileNotFoundError, IndexError):
        pass

    log.debug(f"is_file: {os.path.isfile(old_file_name)}")
    update_logfile_to_device_name(device)


@pytest.fixture(scope="session", autouse=True)
def setup_driver(request):
    print(">>>>>>>>>>> setup driver")
    log.debug(">>>>>>>>>>> setup driver")

    log.info(f'Test Device: {os.environ["DEVICE"]}')

    app.install_app()
    try:
        Preconditions().close_main_botton_sheet()
    except TimeoutException as e:
        if os.environ["PLATFORM"] == "ios":
            pass
        else:
            raise TimeoutException(e)

    # 테스트 중 스크롤 동작 시, gnb 영역 위부터 선택하도록 하기 위해 좌표값을 미리 받아옴
    Preconditions().set_gnb_y()

    print(">>>>>>>>>>> setup driver completed")
    log.debug(">>>>>>>>>>> setup driver completed")


@pytest.fixture(scope="function", autouse=True)
def init_testcase(request):
    global testcase
    testsuite = request.cls.__name__
    testcase = request.function.__name__

    print(f">>>>>>>>>>> init_testcase: {testcase}")
    log.debug(f">>>>>>>>>>> init_testcase: {testcase}")

    app.activate_app_with_recording()

    time_started = time.time()

    # 권한설정 등의 사전 조건 test 함수가 아닌 경우만 수행 되도록 분기
    if "precondition" not in request.keywords:
        yield

        print(">>>>>>>>>>> close_testcase")
        log.debug(">>>>>>>>>>> close_testcase")

        testcase_duration = round(time.time() - time_started, 2)
        print(f"[report][testcase]: {testsuite}>{testcase}|duration: {testcase_duration}")
        log.info(f"[report][testcase]: {testsuite}>{testcase}|duration: {testcase_duration}")

        if os.environ["PLATFORM"] == "ios" and testcase == "test_assets_login":
            time.sleep(5)
        app.close_app_with_recording(testsuite, testcase, values.tc_result)

        print(">>>>>>>>>>> teardown testcase")
        log.debug(">>>>>>>>>>> teardown testcase")


@pytest.fixture(scope="session", autouse=True)
def teardown_driver():
    yield
    print(">>>>>>>>>>> teardown driver")
    log.debug(">>>>>>>>>>> teardown driver")

    app.close_app()


@pytest.fixture(scope="function")
def go_to_assets():
    AssetsPage().go_to_assets()


@pytest.fixture(scope="function")
def go_to_identity_verification():
    AssetsPage().go_to_identity_verification()


@pytest.fixture(scope="function")
def go_to_trade():
    TradePage().go_to_trade()
