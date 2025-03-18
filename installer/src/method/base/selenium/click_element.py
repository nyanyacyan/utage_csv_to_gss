# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time, re, os, json
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import datetime
from typing import Dict, Any, List, Tuple
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException
from pathlib import Path



# 自作モジュール
from method.base.utils.logger import Logger
from method.base.utils.path import BaseToPath
from method.base.utils.popup import Popup
from method.base.selenium.get_element import GetElement

from method.base.decorators.decorators import Decorators
from method.base.Archive.textManager import TextManager
from method.base.selenium.driverDeco import ClickDeco
from method.base.selenium.driverWait import Wait

# const
from method.const_str import ErrorComment

decoInstance = Decorators()


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class ClickElement:
    def __init__(self, chrome: WebDriver):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.get_element = GetElement(chrome=self.chrome)
        self.currentDate = datetime.now().strftime("%y%m%d_%H%M%S")
        self.textManager = TextManager()
        self.clickWait = ClickDeco()
        self.wait = Wait(chrome=self.chrome)
        self.path = BaseToPath()
        self.popup = Popup()

    # ----------------------------------------------------------------------------------
    # クリックしてから入力

    @decoInstance.funcBase
    def clickClearInput(self, value: str, inputText: str, by: str = "xpath"):
        # self.clickWait.canWaitClick(chrome=self.chrome, by=by, value=value, timeout=3)  # 反応しないことが多数。。
        element = self.get_element.getElement(by=by, value=value)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.logger.debug(f"popupなどでClickができません: {element}")
            self.chrome.execute_script("arguments[0].click();", element)

        element.clear()

        try:
            element.send_keys(inputText)

        # chromeDriverのバージョンが対応してない文字を検知した場合
        except WebDriverException as e:
            if "ChromeDriver only supports characters in the BMP" in str(e):
                self.logger.warning(f'chromeDriverのバージョンが対応してない文字を検知: {inputText}')

                bmp_text = ''.join(c for c in inputText if ord(c) < 0x10000)
                self.logger.debug(f'bmp_text: {bmp_text}')
                element.send_keys(bmp_text)

                non_bmp_text = ''.join(c for c in inputText if ord(c) >= 0x10000)
                self.logger.debug(f'non_bmp_text: {non_bmp_text}')
                safe_non_bmp_text = json.dumps(non_bmp_text)
                safe_non_bmp_text = safe_non_bmp_text.strip('"')
                self.chrome.execute_script(f"arguments[0].value += '{safe_non_bmp_text}'", element)
            else:
                self.logger.error(f'未知のWebDriverExceptionが発生しました: {e}')
                return None

        except Exception as e:
            self.logger.error(f'【開発者に連絡してください】入力の際にエラーが発生: {e}')
            return None

        self.clickWait.jsPageChecker(chrome=self.chrome)
        return element

    # ----------------------------------------------------------------------------------
    # 特殊な文字にも対応、クリックしてから入力

    @decoInstance.funcBase
    def clickClearJsInput(self, value: str, inputText: str, by: str = "xpath"):
        self.clickWait.canWaitClick(chrome=self.chrome, by=by, value=value, timeout=3)
        element = self.get_element.getElement(by=by, value=value)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.logger.debug(f"popupなどでClickができません: {element}")
            self.chrome.execute_script("arguments[0].click();", element)
            self.logger.info(f"jsにてクリック実施: {element}")

        element.clear()
        self.chrome.execute_script("arguments[0].value = arguments[1];", element, inputText)
        self.clickWait.jsPageChecker(chrome=self.chrome)
        return element

    # ----------------------------------------------------------------------------------
    # クリックのみ

    def clickElement(self, value: str, by: str = "xpath"):
        self.clickWait.jsPageChecker(chrome=self.chrome)
        element = self.get_element.getElement(by=by, value=value)
        try:
            element.click()
            self.logger.debug(f"クリック完了しました: {value}")
        except ElementClickInterceptedException:
            self.logger.debug(f"popupなどでClickができません: {element}")
            self.chrome.execute_script("arguments[0].click();", element)

        except ElementNotInteractableException:
            self.logger.debug(f"要素があるんだけどクリックができません: {element}")
            self.chrome.execute_script("arguments[0].click();", element)
            self.logger.info(f"jsにてクリック実施: {element}")

            # ✅ ① `display: block;` にせず `visibility: visible;` のみにする
            # self.chrome.execute_script("arguments[0].style.visibility = 'visible';", element)

            # ✅ ② スクロールしてからクリック
            # self.chrome.execute_script("arguments[0].scrollIntoView(true);", element)

            # ✅ ④ JavaScript `dispatchEvent()` でクリックを発火
            # self.chrome.execute_script("""
            #     let event = new MouseEvent('click', {bubbles: true, cancelable: true, view: window});
            #     arguments[0].dispatchEvent(event);
            # """, element)
        except NoSuchElementException:
            self.logger.warning(f'クリックする要素が見つかりません: {element}')
            return None

        self.clickWait.jsPageChecker(chrome=self.chrome)
        return element

    # ----------------------------------------------------------------------------------
    # クリックのみ(要素は別で取得)

    def _click_only(self, web_element: WebElement):
        try:
            web_element.click()
            self.logger.debug(f"クリック完了しました: {web_element}")

        except ElementClickInterceptedException:
            self.logger.debug(f"popupなどでClickができません: {web_element}")
            self.chrome.execute_script("arguments[0].click();", web_element)

        except ElementNotInteractableException:
            self.logger.debug(f"要素があるんだけどクリックができません: {web_element}")
            self.chrome.execute_script("arguments[0].click();", web_element)
            self.logger.info(f"jsにてクリック実施: {web_element}")

        self.clickWait.jsPageChecker(chrome=self.chrome)
        return web_element

    # ----------------------------------------------------------------------------------
    # POPUPがあるかどうかを判断してクリック

    def _handle_popup_click(self, by: str, value: str):
        try:
            check_element = self.get_element.getElement(by=by, value=value)
            if check_element:
                self.logger.info(f'POPUPを発見: {check_element}')
                self.element._click_only(web_element=check_element)

        except NoSuchElementException:
            self.logger.info(f'POPUPはありませんでした。')

        self.clickWait.jsPageChecker(chrome=self.chrome)

    # ----------------------------------------------------------------------------------

    def recaptcha_click_element(
        self, by: str, value: str, home_url: str, check_element_by: str, check_element_value: str, max_retry: int = 40, delay: int = 5
    ):
        self.clickWait.canWaitClick(chrome=self.chrome, by=by, value=value, timeout=3)
        element = self.get_element.getElement(by=by, value=value)

        retry_count = 0
        while retry_count < max_retry:
            try:
                if element:
                    element.click()
                    self.logger.debug(f"クリック完了しました: {value}")
                else:
                    # クリックしてページを移動したけど移動しきれてない例外処理
                    self.logger.warning(f'ログインボタンがありません: {value}')
                    self.chrome.get(home_url)
                    return

                try:
                    # 次のページに移動してるかを確認してるかを確認する例外処理
                    check_element = self.wait.loadPageWait(by=check_element_by, value=check_element_value)
                    if check_element:
                        self.logger.info(f'新しいページに移行しました: {check_element_value}')
                        return self.clickWait.jsPageChecker(chrome=self.chrome)
                except TimeoutException:
                    self.logger.warning("クリックした後に新しいページへの移行できてません。再度クリックします。")

            except ElementClickInterceptedException:
                retry_count += 1
                self.logger.debug(
                    f"画像選択する reCAPTCHA発生中（{retry_count}回目）{delay}秒ごとに継続監視中"
                )
                time.sleep(delay)
                continue

        self.logger.error(f'reCAPTCHA処理が{delay * max_retry}秒を超えましたため終了')

    # ----------------------------------------------------------------------------------

    def _push_enter_key(self, web_element: WebElement):
        web_element.send_keys(Keys.ENTER)
        self.logger.info(f'enter keyの入力しました。')

    # ----------------------------------------------------------------------------------

    def _push_tab_key(self, web_element: WebElement):
        web_element.send_keys(Keys.TAB)
        self.logger.info(f'tab keyの入力しました。')

    # ----------------------------------------------------------------------------------

    def _push_enter_key_none(self, web_element: WebElement):
        self.unlockDisplayNone()
        web_element.send_keys(Keys.ENTER)
        self.logger.info(f'enter keyの入力しました。')

    # ----------------------------------------------------------------------------------

    def _push_tab_key_none(self, web_element: WebElement):
        self.unlockDisplayNone()
        web_element.send_keys(Keys.TAB)
        self.logger.info(f'tab keyの入力しました。')

    # ----------------------------------------------------------------------------------
    # display:noneを解除

    def unlockDisplayNone(self):
        elements = self._searchDisplayNone
        for element in elements:
            if "display: none" in element.get_attribute("style"):
                self.chrome.execute_script(
                    "arguments[0].style.display='block';", element
                )
                self.logger.info(f"display: noneになってる部分を解除実施: {element}")

            else:
                self.logger.debug(f"display: noneになっている部分はありません")

    # ----------------------------------------------------------------------------------

    @property
    def _searchDisplayNone(self):
        return self.getElements(
            by="xpath", value="//*[contains(@style, 'display: none')]"
        )


# ----------------------------------------------------------------------------------

    def _js_tab_key_enter_key_action(self):
        self.chrome.execute_script("""
            document.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Tab'}));
            setTimeout(() => {
                document.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter'}));
            }, 500);  // 0.5秒後に `Enter` を押す
        """)
