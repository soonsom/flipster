# Flipster Test Automation for iOS and Android
* * *
- Selenium Grid 3.141.59
- Appium v.2.7.1
- Python3 v3.8 이상
- Pytest 7.1.3 이상
- FFmpeg 5.1.2 이상 (converting video)

## Installations
* * *
#### Appium
- https://appium.io/


#### Selenium Grid
```
$ selenium-server-standalone-3.141.59.jar
```

#### Pytest
- https://pypi.org/project/pytest/

#### pip install
```
$ pip install -r requirements.txt
```


## Execution
* * *
### 1. Selenium Grid & 수행할 장비 별 Appium Server 실행
```commandline
# 1. open cmd to run selenium grid
cd ./selenium_grid/starthub.sh

# 2. open another cmd to run an appium server for device A
cd ./devices/iphonexr #테스트 할 장비명 A

# 3. open another cmd to run an appium servere for device B
cd ./devices/galaxys21 #테스트 할 장비명 B
```
### 2. 테스트 수행에 필요한 .env 파일 생성하기
- **`setup.sh` 수행 시**
> - `testinfo-{device}.env`, ``testinfo-run.env 파일이 생성되며 해당 파일에 저장된 환경변수 정보로 E2E 테스트가 수행된다.
- 아래 정보를 입력 후 setup.sh를 실행한다. (모든 변수는 소문자로 입력)

| Parameter   | Decription                                                                                                                          | Vale1 | Value2            |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------|------|-------------------|
| PLATFORM    | 수행할 플랫폼                                                                                                                             | ios  | android           |
| DEVICE      | - 수행할 장비: json으로 추가된 장비 중에서 선택 <br> - 장비 추가시 json 및 appium 실행 cmdline이 저장된 파일 2개를 동일한 장비명으로 생성해야 한다.<br> - iphonexr, iphponexr.json | iphonexr | galaxys21         |
| BALANCE     | 계정의 BALANCE 값                                                                                                                       | 0.00 ||
| TOTAL VALUE | 계정의 TOTAL VALUE 값                                                                                                                   | 0.00 ||
| DEBUG_MODE     | - traceback 에서 print문을 보고 싶은경우: 0 <br> - html report를 생성하고 싶은 경우: 1 (traceback에서 print문 출력이 되지 않음)                                  | 0    | 1                 |
| KEYWORD_TC     | 테스트를 수행할 함수명 입력                                                                                                                     | test | test_assets_login |

```
$ ./setup.sh ${PLATFORM} ${DEVICE} ${ID} ${PASSWORD} ${BALANCE} ${TOTAL_VALUE}

# e.g.
$ ./seteup.sh ios iphonexr yourid yourpw 0.00 0.00
```


### 3. pytest 수행하기
* run.sh 실행하여 pytest 스크립트 수행
```commandline
$ ./run.sh ${PLATFORM} ${DEVICE} ${DEBUG_MODE} "${KEYWORD_TC}"

# e.g. 
$ run.sh iphonexr "test" 0 ios
```

### *(optional) 4. 장비명으로 log 파일 저장 및 mp4 파일 압축하기* 
* cleanup.sh 실행
```
$ ./cleanup.sh ${DEVICE}

# e.g.
$ ./cleanup.sh iphonexr
```

## Reports
* * *
테스트 수행 완료 후 results 폴더에 TestReport.html 및 mp4 파일들이 생성된다.
- `results/{platform}/`
  - `TestReport_{platrom}{os verion}_{device}.html`: TestCase 별 스텝 및 screenshot
    - e.g. `TestReport_ios15.5_iphonexr`
  - `mp4`: TestCase 별로 mp4 파일이 생성된다.
    - `{device}/{passed}/{test suite}/{platform}{os veresion}_{testcase}.mp4` 
    - `{device}/{failed}/{test suite}/{platform}{os veresion}_{testcase}.mp4`
    - e.g. `iphonexr/passed/TestAssets/android12.0_test_assets_login.mp4`
