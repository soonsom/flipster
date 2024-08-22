import argparse
import os
import zipfile

from dotenv import load_dotenv

from utils.filehandlers import load_json, make_directory


def zip_recordings(device):
    capabilities = load_json(f'./devices/{device.lower()}.json')
    platform = os.environ["PLATFORM"]
    platform_version = capabilities['capabilities'][0]['platformVersion']

    results = ["passed", "failed"]
    for result in results:
        path = os.path.abspath(f"./results/{platform}/{device}/{result}")
        zip_filename = f"Recordings_{platform}{platform_version}_{device}_{result}.zip"

        try:
            fantasy_zip = zipfile.ZipFile(path+"/"+zip_filename, 'w')
            for folder, subfolders, files in os.walk(path):
                for file in files:
                    if file.endswith('.mp4'):
                        fantasy_zip.write(os.path.join(folder, file),
                                          os.path.relpath(os.path.join(folder, file), path),
                                          compress_type=zipfile.ZIP_DEFLATED)
            fantasy_zip.close()
            print(f"saved result files: {os.listdir(path)}")

        except FileNotFoundError as e:
            print(e)


# Parallel로 multi device 수행 시, log 파일이 hex 파일 명으로 여러개 생성되어
# 불필요한 로그파일을 제외하고 실제 수행 장비의 로그 파일만 얻어오기 위한 함수
def update_logfile_to_device_name(device):
    dir_path = f"./logs/{os.environ['PLATFORM']}"
    try:
        file_list = os.listdir(dir_path)
    except FileNotFoundError:
        make_directory(dir_path)

    new_file_name = os.path.abspath(f'{dir_path}/{device}.log')
    for file in file_list:
        old_file_name = os.path.abspath(f'{dir_path}/{file}')
        f = open(old_file_name, encoding='utf-8')
        readline = 1
        while readline <= 100:
            line = f.readline()
            readline += 1
            if f"Test Device: {device}" == line.strip() and old_file_name != new_file_name:
                f.close()
                os.rename(old_file_name, new_file_name)
                print(f"log file name: {new_file_name}")
                print(f"log files: {[filename for filename in file_list]}")

                return new_file_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='--device')
    parser.add_argument('--device', required=True)
    args = parser.parse_args()

    load_dotenv(os.path.abspath(f'./testinfo-run.env'))

    print(update_logfile_to_device_name(args.device))
    print(zip_recordings(args.device))
