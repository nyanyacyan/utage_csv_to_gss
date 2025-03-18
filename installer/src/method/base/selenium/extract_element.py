# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time, re, os, json
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from datetime import datetime
from typing import Dict, Any, List, Tuple
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException
from method.base.utils.time_manager import TimeManager


# 自作モジュール
from method.base.utils.logger import Logger
from method.base.utils.path import BaseToPath
from method.base.utils.popup import Popup

from method.base.decorators.decorators import Decorators
from installer.src.method.base.selenium.get_element import GetElement
from method.base.Archive.textManager import TextManager
from method.base.selenium.driverDeco import ClickDeco
from method.base.selenium.driverWait import Wait

# const
from method.const_str import ErrorComment

decoInstance = Decorators()


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class ExtractElement:
    def __init__(self, chrome: WebDriver):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.currentDate = datetime.now().strftime("%y%m%d_%H%M%S")
        self.get_element = GetElement(chrome=self.chrome)
        self.textManager = TextManager()
        self.time_manager = TimeManager()

        self.wait = Wait(chrome=self.chrome)
        self.path = BaseToPath()
        self.popup = Popup()

    # ----------------------------------------------------------------------------------
    # 大カテゴリ、中カテゴリの抽出

    def _category_major_to_medium(self, path_info: Dict):
        # 大カテゴリの読込
        link_text_list, link_url_list = self.get_element._get_link_text_list(by=path_info['MAJOR_BY'], value=path_info['MAJOR_VALUE'])

        category_list = []

        # 大カテゴリごとにアクセスして中カテゴリを読み込む
        for i, link_url in enumerate(link_url_list):
            self.chrome.get(url=link_url)
            self.time_manager._random_sleep()

            medium_category_element = self.get_element.getElements(by=path_info['MEDIUM_BY'], value=path_info['MEDIUM_VALUE'])

            medium_category_text_list = self.get_element._extract_text_list(web_elements=medium_category_element)

            # 中カテゴリを抽出
            for text in medium_category_text_list:
                self.logger.debug(f'\n大カテゴリ: {link_text_list[i]}\n中カテゴリ: {text}')

                # 大カテゴリと中カテゴリのtupleをリストに入れていく
                category_list.append((link_text_list[i], text))

            self.logger.debug(f'[i]個目の大カテゴリの中カテゴリリスト: {category_list}')

        # デバッグ用
        if category_list:
            for category_tuple in category_list[:10]:  # 10個まで
                self.logger.info(f': {category_tuple}')

        return category_list

    # ----------------------------------------------------------------------------------
