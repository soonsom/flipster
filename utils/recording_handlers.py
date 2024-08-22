from utils.logger import log
import os
import base64

from base import app
from utils.filehandlers import make_directory


def save_recording(raw_recording, file_name, directory):
    print(f"save_recording > directory: {directory}")
    log.debug(f"save_recording > file_name: {file_name}")
    path = make_directory(f'./results/{os.environ["PLATFORM"]}/{os.environ["DEVICE"]}/{directory}')
    file_name = f'{file_name}.mp4'
    with open(os.path.join(path, file_name), "wb") as recording:
        return recording.write(base64.b64decode(raw_recording))


def stop_recording(testsuite_name, testcase_name, result):
    print(f"stop_recording > testsuite: {testsuite_name}")
    log.debug(f"stop_recording > testcase: {testcase_name}")
    raw_recording = app.driver.stop_recording_screen()
    platform = os.environ["PLATFORM"]
    platform_version = os.environ["OS_VERSION"]
    file_name = f'{platform}{platform_version}_{testcase_name}'
    save_recording(raw_recording, file_name, f"{result}/{testsuite_name}")  #녹화 종료 및 저장
