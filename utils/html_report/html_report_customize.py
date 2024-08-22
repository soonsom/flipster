import os

from py.xml import html
import pytest

from base import app
from common import values
from base.setup_capabilities import desired_capabilities_setup as capabilities

count_failed = 0
count_passed = 0
count_skipped = 0

testcase_executed = ""
slack_thread_ts = ""


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    platform = os.environ['PLATFORM']
    device = os.environ["DEVICE"]
    platform_version = capabilities(os.environ["DEVICE"])['platformVersion']
    session.config._metadata = {
        "Test platform": f"{platform} {platform_version}",
        "Test device": device,
    }


def pytest_html_report_title(report):
    report.title = f"{os.environ['PLATFORM']} App Regression Test"


def pytest_html_results_summary(prefix, summary, postfix):
    global count_failed
    prefix.extend([html.p(f"- Passed: {count_passed} / Failed(Errors): {count_failed} / Skipped: {count_skipped}", class_="error-summary")])

    pf_rate = count_passed/(count_passed+count_failed)*100
    prefix.extend([html.p(f"- Pass Rate: {round(pf_rate, 0)}%", class_="error-summary")])


def pytest_html_results_table_header(cells):
    del cells[1]
    cells.insert(1, html.th("Test Suite", class_="testsuite"))
    cells.insert(2, html.th("TestCase"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    font_color = ""
    if report.failed:
        font_color = "font-color-error"
    elif report.skipped:
        font_color = "font-color-skipped"

    del cells[1]
    cells.insert(1, html.td(report.testsuite, class_=font_color))
    cells.insert(2, html.td(report.testcase, class_=font_color))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    report.testsuite = str(item.cls.__name__)
    report.testcase = str(item.function.__name__)
    extra = getattr(report, "extra", [])
    blocked_msg = ""
    global testcase_executed, slack_thread_ts

    steps = []
    screenshots = []
    case_id = 0

    if report.when == "setup" and report.failed:
        values.tc_result = "blocked"

        blocked_msg = f"테스트 진입 실패. \n> 테스트 할 대상의 진입 스텝이나 인터넷 연결에 이상이 있는지 확인해 주세요."

    else:
        values.tc_result = "untested"

    if report.when == "call":
        values.tc_result = report.outcome
        extra.append(pytest_html.extras.html("<table width=100% style='border:none'>"))
        last_screenshot = ""
        if report.passed:
            for index, step in enumerate(app.steps, 1):
                html_steps = f'<tr style="border-bottom: 1px solid #E6E6E6"> \
                                <td style="border:none; vertical-align:top; width:70%"> \
                                    {index}. {step} \
                                </td> \
                            </tr>'

                extra.append(pytest_html.extras.html(html_steps))

            extra.append(pytest_html.extras.html("</table>"))

            app.steps = []
            app.screenshots = []

        else:
            print(f"[testcase]: {report.testcase}")
            print(f"[app steps]: {app.steps}, {len(app.steps)}")
            print(f"[app screenshots]: {len(app.screenshots)}")
            for index, (step, screenshot) in enumerate(zip(app.steps, app.screenshots), 1):
                html_steps = f'<tr style="border-bottom: 1px solid #E6E6E6"> \
                                <td style="border:none; vertical-align:top; width:70%"> \
                                    {index}. {step} \
                                </td> \
                                <td style="padding-right: 30px; border: none"> \
                                    <img onclick="javascript:document.getElementById(\'show_{report.testsuite}_{report.testcase}_{index}\').style.display=\'block\'" align="right" margin-right="100px" width="160px" src="data:image/png;base64, {screenshot}" /> \
                                    <div id="show_{report.testsuite}_{report.testcase}_{index}" class="show-popup" onclick="javascript:this.style.display=\'none\'"> \
                                        <img class="show-image" src = "data:image/png;base64, {screenshot}" />\
                                    </div> \
                                </td> \
                            </tr>'

                extra.append(pytest_html.extras.html(html_steps))

            extra.append(pytest_html.extras.html("</table>"))

    # pytest에서 FAILED: report.afiled, ERROR: report.outcome==failed로 떨어짐
    # failed/error인 경우 한번 더 스크린샷을 남겨서 error log에 포함
    if report.failed:
        error_msg = report.longreprtext

        try:
            last_screenshot = app.driver.get_screenshot_as_base64()
        except Exception as e:
            print(f"마지막 스크린샷 오류, {e}")
            try:
                last_screenshot = app.screenshots[-1]
            except IndexError:
                last_screenshot = ""

        html_failed_img = f'<div>' \
                          f'<img src="data:image/png;base64, {last_screenshot}" width= "225px" onclick="javascript:document.getElementById(\'show_{report.testcase}\').style.display=\'block\'" align="right"/>' \
                          f'</div>' \
                          f'<div id="show_{report.testcase}" class="show-popup" onclick="javascript:this.style.display=\'none\'"> \
                                                <img class="show-image" src = "data:image/png;base64, {last_screenshot}" /> \
                                            </div>'
        extra.append(pytest_html.extras.html(html_failed_img))

        values.tc_result = "failed"

        testcase_executed = report.testcase

        app.steps = []
        app.screenshots = []

    report.extra = extra


def pytest_html_results_table_html(report, data):
    global count_passed
    global count_failed
    global count_skipped

    if report.passed:
        count_passed += 1
        del data[-1]
    elif report.failed:
        count_failed += 1
    elif report.skipped:
        count_skipped += 1
