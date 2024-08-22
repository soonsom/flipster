import os

from appium import webdriver

from utils.recording_handlers import stop_recording
from base.setup_capabilities import desired_capabilities_setup

driver = None
steps = []
screenshots = []

package = {
    "ios": "com.aqx.prex",
    "android": "com.prestolabs.android.prex"
}


def install_app():
    global driver
    if driver is None:
        driver = webdriver.Remote(desired_capabilities=desired_capabilities_setup(os.environ["DEVICE"]))
        driver.start_recording_screen(videoFps=100, timeLimit=20 * 60)


def activate_app_with_recording():
    global driver
    activate_app()
    driver.start_recording_screen(videoFps=100, timeLimit=20*60)


def activate_app():
    global driver
    driver.activate_app(package[os.environ["PLATFORM"]])


def close_app_with_recording(testsuite_name, testcase_name, result):
    close_app()
    stop_recording(testsuite_name, testcase_name, result)


def close_app():
    global driver
    driver.terminate_app(package[os.environ["PLATFORM"]])
