import logging
import os
import uuid

from dotenv import load_dotenv
load_dotenv(os.path.abspath(f'./testinfo-run.env'))

# 멀티 장비 parallel 수행 시, 동일한 이름으로 log 파일이 생성되는 것 방지
unique_hex = uuid.uuid4().hex
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f"logs/{os.environ['PLATFORM']}/logs-{unique_hex}.log", encoding="utf-8")
log.addHandler(file_handler)
