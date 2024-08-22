import os
from time import sleep

from base import app
from utils.enums import ScreenshotPosition
from utils.logger import log


class Screenshot(object):
    def __init__(self, note=None, screenshot_position=ScreenshotPosition.POST, wait=1):
        self.note = note
        self.wait = wait
        self.screenshot_position = screenshot_position

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            steps = f'{args[0].__class__.__name__} > {func.__name__}'

            if self.note is not None:
                steps = f'{args[0].__class__.__name__} > {func.__name__}({self.note})'

            if self.screenshot_position == ScreenshotPosition.POST:
                return_func = func(*args, **kwargs)

            sleep(self.wait)  # to wait for a quick change of the screen
            screenshot = app.driver.get_screenshot_as_base64()
            app.screenshots.append(screenshot)
            log.debug(f" >>>>>>>>>>> screenshot: {screenshot[:5]}")
            log.debug(f" >>>>>>>>>>> app.screenshots: {app.screenshots[0][:5]}")
            app.steps.append(steps)

            if self.screenshot_position != ScreenshotPosition.POST:
                return_func = func(*args, **kwargs)

            log.debug(f" >>>>>>>>>>> app.steps: {app.steps}")

            return return_func

        return wrapper
