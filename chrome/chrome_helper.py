#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from log_handle import logger
import logging
import zipfile
import requests
import file_util

# https://medium.com/drunk-wis/python-selenium-chrome-browser-%E8%88%87-driver-%E6%83%B1%E4%BA%BA%E7%9A%84%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86-cbaf1d1861ce
CHROME_DRIVER_BASE_URL = "https://chromedriver.storage.googleapis.com"
CHROME_DRIVER_FOLDER = r".\chrome"
CHROME_DRIVER_MAPPING_FILE = r"{}\mapping.json".format(CHROME_DRIVER_FOLDER)
CHROME_DRIVER_EXE = r"{}\chromedriver.exe".format(CHROME_DRIVER_FOLDER)
CHROME_DRIVER_ZIP = r"{}\chromedriver_win32.zip".format(CHROME_DRIVER_FOLDER)


def init_dir():
    if not os.path.exists(CHROME_DRIVER_FOLDER):
        os.makedirs(CHROME_DRIVER_FOLDER)


def get_chrome_driver_major_version():
    chrome_browser_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_ver = file_util.get_file_version(chrome_browser_path)
    logger.info(f'chrome version is {chrome_ver}')
    chrome_major_ver = chrome_ver.split(".")[0]
    logger.info(f'chrome driver major version is {chrome_major_ver}')
    return chrome_major_ver


def get_latest_driver_version(browser_ver):
    latest_api = "{}/LATEST_RELEASE_{}".format(
        CHROME_DRIVER_BASE_URL, browser_ver)
    logger.info(f'latest api is {latest_api}')
    resp = requests.get(latest_api)
    lastest_driver_version = resp.text.strip()
    logger.info(f'latest driver version is {lastest_driver_version}')
    return lastest_driver_version


def download_driver(driver_ver, dest_folder):
    download_api = "{}/{}/chromedriver_win32.zip".format(
        CHROME_DRIVER_BASE_URL, driver_ver)
    logger.info(f'download api is {download_api}')
    dest_path = os.path.join(dest_folder, os.path.basename(download_api))
    resp = requests.get(download_api, stream=True, timeout=300)
    logger.info(f'download dest path is {dest_path}')
    if resp.status_code == 200:
        with open(dest_path, "wb") as f:
            f.write(resp.content)
        logger.info("Download driver completed")
    else:
        raise Exception("Download chrome driver failed")


def unzip_driver_to_target_path(src_file, dest_path):
    with zipfile.ZipFile(src_file, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
    logger.info("Unzip [{}] -> [{}]".format(src_file, dest_path))


def read_driver_mapping_file():
    driver_mapping_dict = {}
    if os.path.exists(CHROME_DRIVER_MAPPING_FILE):
        driver_mapping_dict = file_util.read_json(CHROME_DRIVER_MAPPING_FILE)
    logger.info(f'driver mapping dict is {driver_mapping_dict}')
    return driver_mapping_dict


def check_browser_driver_available():
    chrome_major_ver = get_chrome_driver_major_version()
    mapping_dict = read_driver_mapping_file()
    driver_ver = get_latest_driver_version(chrome_major_ver)

    if chrome_major_ver not in mapping_dict:
        download_driver(driver_ver, CHROME_DRIVER_FOLDER)
        unzip_driver_to_target_path(CHROME_DRIVER_ZIP, CHROME_DRIVER_FOLDER)

        mapping_dict = {
            chrome_major_ver: {
                "driver_path": CHROME_DRIVER_EXE,
                "driver_version": driver_ver
            }
        }
        mapping_dict.update(mapping_dict)
        file_util.write_json(CHROME_DRIVER_MAPPING_FILE, mapping_dict)


if __name__ == "__main__":
    init_dir()
    check_browser_driver_available()
