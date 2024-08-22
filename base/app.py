import os

from appium import webdriver

from base.setup_capabilities import desired_capabilities_setup


def install_app():
    global driver
    if driver is None:
        driver = webdriver.Remote(desired_capabilities=desired_capabilities_setup(os.environ["DEVICE"]))
        driver.start_recording_screen(videoFps=100, timeLimit=20 * 60)
