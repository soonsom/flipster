import sys
import os
import argparse

from dotenv import load_dotenv
from flask import Flask, render_template

sys.path.append(os.path.abspath("./"))
from utils.logger import log

app = Flask(__name__)


def get_executed_testcases_and_duration(devices):
    testcases_with_duration = {}

    for device in devices:
        testcases_with_duration[device] = []
        f = open(os.path.abspath(f"./logs/{os.environ['PLATFORM']}/{device}.log"), "r")
        deli = "[report][testcase]:"

        while True:
            line = f.readline()
            if deli in line.strip():
                testcases_with_duration[device].append(line.strip().split(deli)[-1])

            elif not line:
                break

        f.close()

    return testcases_with_duration


def get_major_executed_testcases(testcases):
    testcases_count = []
    for key in testcases.keys():
        testcases_count.append(len(testcases[key]))

    testcases_count.sort()
    print(f"testcases_count: {testcases_count}")

    for key in testcases.keys():
        if testcases_count[-1] == len(testcases[key]):
            return testcases[key]


# final result: n passed, n failed, n rerun n skipped / total n in (mm:hh:ss)
def get_final_test_results(devices):
    test_results = {}
    for device in devices:
        test_results[device] = []
        f = open(os.path.abspath(f"./logs/{os.environ['PLATFORM']}/{device}.log"), "r")
        while True:
            line = f.readline()
            if "[report][summary]:" in line.strip():
                test_results[device].append(line.split("[summary]:")[-1].strip())

            elif not line:
                print(f"{device} result: {len(test_results[device])}")
                if len(test_results[device]) == 0:
                    test_results[device].append("0 passed, 0 failed, 0 error, 0 skipped, 0 rerun / total: 0")
                break

        f.close()
    return test_results


def get_pass_rates(devices):
    result_summaries = get_final_test_results(devices)
    pass_rates = {}
    passed_count = 0

    for device in devices:
        pass_rates[device] = []
        try:
            result = result_summaries[device][0].split("/")
            status_list = result[0].split(",")

            if "passed" in status_list[0]:
                passed_count = int(status_list[0].split("passed")[0].strip())

            total_count = int(result[-1].split("total:")[-1].split("in")[0].strip())

            try:
                pass_rate = round((passed_count/total_count)*100, 2)
            except ZeroDivisionError:
                pass_rate = 0

        except IndexError:
            print(f"{device} is not properly worked. Check if INTERNAL ERROR has occurred")
            log.info(f"{device} is not properly worked. Check if INTERNAL ERROR has occurred")
            # 장비 연결 끊김 이슈 발생 시, pass_rate를 임의로 0으로 설정.
            # 추후 N/A로 입력하여 수치 변경하도록 수정 예정
            pass_rate = 0

        pass_rates[device].append(pass_rate)

    return pass_rates


def get_total_pass_rate(pass_rates):
    pass_rate_numerator = 0
    print(pass_rates)
    for key in pass_rates.keys():
        pass_rate_numerator += pass_rates[key][0]

    pass_rate = round(pass_rate_numerator/len(pass_rates), 2)

    return pass_rate


# get <TestReport> testcase name: class and function name
# get <TestReport> test result: pass, failed, errors, rerun, skipped
def get_testcase_summaries(devices):
    testcase_summaries = {}
    for device in devices:
        testcase_summaries[device] = []
        f = open(os.path.abspath(f"./logs/{os.environ['PLATFORM']}/{device}.log"), "r")
        deli = "[report][testcase_summary]:"

        while True:
            line = f.readline()
            if deli in line.strip():
                testcase_summaries[device].append(line.strip().split(deli)[-1])

            elif not line:
                break

        f.close()
    return testcase_summaries


@app.route('/')
def make_html_report(devices):
    devices = devices.replace("[", "").replace("]", "").replace(" ", "").split(",")
    platform_versions = []
    testcases_with_durations = get_executed_testcases_and_duration(devices)
    major_testcases = get_major_executed_testcases(testcases_with_durations)
    testcase_summaries = get_testcase_summaries(devices)
    test_final_results = get_final_test_results(devices)
    print(f"test_final_results: {test_final_results}")
    pass_rates = get_pass_rates(devices)
    total_pass_rate = get_total_pass_rate(pass_rates)

    for device in devices:
        load_dotenv(os.path.abspath(f'./testinfo-{device}.env'))
        platform = os.environ["PLATFORM"]
        app_version = os.environ["APP_VERSION"]
        platform_versions.append(os.environ["OS_VERSION"])

    with app.app_context():
        html_output = render_template('template.html',
                                      app_version=app_version,
                                      platform=platform,
                                      devices=devices,
                                      platform_versions=platform_versions,
                                      major_testcases=major_testcases,
                                      testcases_with_durations=testcases_with_durations,
                                      testcase_summaries=testcase_summaries,
                                      test_final_results=test_final_results,
                                      pass_rates=pass_rates,
                                      total_pass_rate=total_pass_rate)

        with open(os.path.abspath(f"./results/{os.environ['PLATFORM']}/TestReport_v{app_version}_{platform}_final_report.html"), "w") as f:
            f.write(html_output)
        return html_output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='--devices')
    parser.add_argument('--devices', required=True)
    args = parser.parse_args()

make_html_report(args.devices)


# app.run('0.0.0.0', port=5010, threaded=True)
