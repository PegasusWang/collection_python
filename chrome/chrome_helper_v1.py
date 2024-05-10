#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import zipfile
import requests

from log_handle import logger
import file_util

CHROME_DRIVER_BASE_URL = "https://storage.googleapis.com/chrome-for-testing-public"
CHROME_DRIVER_FOLDER = r".\chrome"
CHROME_DRIVER_MAPPING_URL = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
CHROME_DRIVER_MAPPING_FILE = f"{CHROME_DRIVER_FOLDER}\mapping.json"
CHROME_DRIVER_EXE = f"{CHROME_DRIVER_FOLDER}\chromedriver.exe"
CHROME_DRIVER_ZIP = f"{CHROME_DRIVER_FOLDER}\chromedriver-win64.zip"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}


def get_chrome_driver_major_version():
    chrome_browser_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_ver = file_util.get_file_version(chrome_browser_path)
    logger.info(f'chrome version is {chrome_ver}')
    chrome_major_ver = chrome_ver.split(".")[0]
    logger.info(f'chrome driver major version is {chrome_major_ver}')
    return chrome_ver


def download_driver(driver_ver, dest_folder):
    download_api = f"{CHROME_DRIVER_BASE_URL}/{driver_ver}/win64/chromedriver-win64.zip"
    logger.info(f'download api is {download_api}')
    dest_path = os.path.join(dest_folder, os.path.basename(download_api))
    # urllib.request.urlretrieve(download_api,dest_path)
    resp = requests.get(download_api)
    logger.info(f'download dest path is {dest_path}')
    if resp.status_code != 200:
        raise Exception("Download chrome driver failed")
    with open(dest_path, "wb") as f:
        # for chunk in resp.iter_content(chunk_size=1024):
        f.write(resp.content)
    logger.info("Download driver completed")


def get_download_chrome_driver_ver(chrome_ver):
    """get download chrome driver version"""
    mapping_dict = read_driver_mapping_file()
    start, end = chrome_ver.rsplit('.', 1)
    for item in mapping_dict['versions']:
        if start in item['version']:
            return item['version']


def unzip_driver_to_target_path(src_file, dest_path):
    """unzip chrome driver to target path"""
    with zipfile.ZipFile(src_file, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
    logger.info(f"Unzip [{src_file}] -> [{dest_path}]")


def download_driver_mapping_file():
    """download driver mapping file"""
    resp = requests.get(CHROME_DRIVER_MAPPING_URL, timeout=300)
    logger.info(f'download dest path is {CHROME_DRIVER_MAPPING_FILE}')
    if resp.status_code != 200:
        raise Exception("Download chrome driver mapping file failed")
    with open(CHROME_DRIVER_MAPPING_FILE, "w") as f:
        f.write(resp.text)
    logger.info("Download driver mapping file completed")


def read_driver_mapping_file():
    """read driver mapping file"""
    driver_mapping_dict = {}
    if os.path.exists(CHROME_DRIVER_MAPPING_FILE):
        driver_mapping_dict = file_util.read_json(CHROME_DRIVER_MAPPING_FILE)
    logger.info(f'driver mapping dict is {driver_mapping_dict}')
    return driver_mapping_dict


def check_browser_driver_available():
    """check if the driver is available"""
    chrome_ver = get_chrome_driver_major_version()
    download_driver_mapping_file()
    download_chrome_version = get_download_chrome_driver_ver(chrome_ver)
    download_driver(download_chrome_version, CHROME_DRIVER_FOLDER)
    unzip_driver_to_target_path(CHROME_DRIVER_ZIP, CHROME_DRIVER_FOLDER)


def main():
    """main function"""
    if not os.path.exists(CHROME_DRIVER_FOLDER):
        os.makedirs(CHROME_DRIVER_FOLDER)
    check_browser_driver_available()


if __name__ == "__main__":
    main()
