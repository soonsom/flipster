import os
from dotenv import load_dotenv

from utils.filehandlers import load_json


def desired_capabilities_setup(device):
    load_dotenv(os.path.abspath(f'./testinfo-{device}.env'))
    capabilities = load_json(f'./devices/{device.lower()}.json')

    # app 파일이 존재하는 경우 아래 코드로 app 경로 지정
    # extension = {
    #     "ios": "ipa",
    #     "android": "apk"
    # }

    # app_path = os.path.abspath(f'./apps/{os.environ["PLATFORM"]}/{os.environ["APP_VERSION"]}.{extension[os.environ["PLATFORM"].lower()]}')

    if os.environ["PLATFORM"] == "ios":
        app = "com.aqx.prex"
        capabilities['capabilities'][0]['app'] = app
    os.environ["OS_VERSION"] = capabilities['capabilities'][0]['platformVersion']

    return capabilities['capabilities'][0]
