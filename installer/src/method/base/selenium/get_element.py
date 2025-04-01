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
from pathlib import Path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.utils.path import BaseToPath
from method.base.utils.popup import Popup

from method.base.decorators.decorators import Decorators
from method.base.utils.textManager import TextManager
from method.base.selenium.driverDeco import ClickDeco
from method.base.selenium.driverWait import Wait

# const
from method.const_str import ErrorComment

decoInstance = Decorators()


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class GetElement:
    def __init__(self, chrome: WebDriver):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.currentDate = datetime.now().strftime("%y%m%d_%H%M%S")
        self.textManager = TextManager()
        self.clickWait = ClickDeco()
        self.wait = Wait(chrome=self.chrome)
        self.path = BaseToPath()
        self.popup = Popup()

    # ----------------------------------------------------------------------------------

    def getElement(self, value: str, by: str = "xpath"):
        self.clickWait.jsPageChecker(chrome=self.chrome)
        if by == "id":
            return self.chrome.find_element(By.ID, value)
        elif by == "css":
            return self.chrome.find_element(By.CSS_SELECTOR, value)
        elif by == "xpath":
            return self.chrome.find_element(By.XPATH, value)
        elif by == "tag":
            return self.chrome.find_element(By.TAG_NAME, value)
        elif by == "link":
            return self.chrome.find_element(By.LINK_TEXT, value)
        elif by == "name":
            return self.chrome.find_element(By.NAME, value)
        elif by == "class":
            return self.chrome.find_element(By.CLASS_NAME, value)
        else:
            raise ValueError("定義してるもの以外のものを指定してます")

    # ----------------------------------------------------------------------------------
    # 複数

    def getElements(self, value: str, by: str = "xpath"):
        self.clickWait.jsPageChecker(chrome=self.chrome)
        if by == "id":
            return self.chrome.find_elements(By.ID, value)
        elif by == "css":
            return self.chrome.find_elements(By.CSS_SELECTOR, value)
        elif by == "xpath":
            return self.chrome.find_elements(By.XPATH, value)
        elif by == "tag":
            return self.chrome.find_elements(By.TAG_NAME, value)
        elif by == "link":
            return self.chrome.find_elements(By.LINK_TEXT, value)
        elif by == "name":
            return self.chrome.find_elements(By.NAME, value)
        elif by == "class":
            return self.chrome.find_elements(By.CLASS_NAME, value)
        else:
            raise ValueError("定義してるもの以外のものを指定してます")

    # ----------------------------------------------------------------------------------
    # 要素を絞り込み

    def filterElement(self, parentElement: WebElement, value: str, by: str = "xpath"):
        self.clickWait.jsPageChecker(chrome=self.chrome)

        if by == "id":
            return parentElement.find_element(By.ID, value)
        elif by == "css":
            return parentElement.find_element(By.CSS_SELECTOR, value)
        elif by == "xpath":
            return parentElement.find_element(By.XPATH, value)
        elif by == "tag":
            return parentElement.find_element(By.TAG_NAME, value)
        elif by == "link":
            return parentElement.find_element(By.LINK_TEXT, value)
        elif by == "name":
            return parentElement.find_element(By.NAME, value)
        elif by == "class":
            return parentElement.find_element(By.CLASS_NAME, value)
        else:
            raise ValueError("定義しているもの以外のものを指定しています")

    # ----------------------------------------------------------------------------------
    # 要素を絞り込み

    def filterElements(self, parentElement: WebElement, value: str, by: str = "xpath"):
        self.clickWait.jsPageChecker(chrome=self.chrome)

        if by == "id":
            return parentElement.find_elements(By.ID, value)
        elif by == "css":
            return parentElement.find_elements(By.CSS_SELECTOR, value)
        elif by == "xpath":
            return parentElement.find_elements(By.XPATH, value)
        elif by == "tag":
            return parentElement.find_elements(By.TAG_NAME, value)
        elif by == "link":
            return parentElement.find_elements(By.LINK_TEXT, value)
        elif by == "name":
            return parentElement.find_elements(By.NAME, value)
        elif by == "class":
            return parentElement.find_elements(By.CLASS_NAME, value)
        else:
            raise ValueError("定義しているもの以外のものを指定しています")

    # ----------------------------------------------------------------------------------
    # 親要素から絞り込んで要素を取得

    def _get_sort_element(self, parent_by: str, parent_path: str, child_by: str, child_path: str):
        parent_element = self.getElement(by=parent_by, value=parent_path)
        child_element = self.filterElement(
            parentElement=parent_element, by=child_by, value=child_path
        )
        self.logger.debug(
            f"\nparent_element: {parent_element}\nchild_element: {child_element}"
        )
        return child_element

    # ----------------------------------------------------------------------------------
    # 親要素から絞り込んで要素を取得

    def _get_link(self, value: str):
        link_web_elements = self.getElements(by='link', value=value)

        if not link_web_elements:
            self.logger.error(f'リンクが見つかりませんでした。')
            return None

        if len(link_web_elements) > 1:
            self.logger.error(f'リンクが2つ以上、見つかりました: {link_web_elements}')
        last_link_web_element = link_web_elements[-1]

        # リンクをデバッグ
        link_url = last_link_web_element.get_attribute('href')
        self.logger.debug(f'link_url: {link_url}')

        return last_link_web_element

    # ----------------------------------------------------------------------------------
    # 親要素から絞り込んで要素を取得

    def _get_link_text_list(self, by: str, value: str):
        link_web_elements = self.getElements(by=by, value=value)

        link_text_list = self._extract_link_list(web_elements=link_web_elements)
        link_url_list = self._extract_link_list(web_elements=link_web_elements)


        return link_text_list, link_url_list

    # ----------------------------------------------------------------------------------
    # webElementsからテキストリストを生成

    def _extract_text_list(self, web_elements: List[WebElement]):
        if not web_elements:
            self.logger.error(f"WebElementがありません。{__name__}")
            return []

        text_list = [element.text for element in web_elements]
        if not text_list:
            self.logger.error(f"WebElementにテキストがありません。{__name__}")

        self.logger.debug(f'抽出されたテキストリスト: {text_list}')
        return text_list

    # ----------------------------------------------------------------------------------
    # webElementsからURLリストを生成

    def _extract_link_list(self, web_elements: List[WebElement]):
        if not web_elements:
            self.logger.error(f"{self.__class__.__name__}: WebElementがありません。")
            return []

        url_list = [element.get_attribute('href') for element in web_elements]

        if not url_list:
            self.logger.error(f"{self.__class__.__name__}: 指定のWebElementにURLがありません。")

        self.logger.debug(f'抽出されたURLリスト: {url_list}')
        return url_list

    # ----------------------------------------------------------------------------------

    # 親要素から絞り込んだ要素からtextを取得

    def _get_sort_element_text(self, parent_path: str, child_path: str):
        scope_element = self._get_sort_element(
            parent_path=parent_path, child_path=child_path
        )
        text = self._get_text(element=scope_element)
        self.logger.debug(f"\nscope_element: {scope_element}\ntext: {text}")
        return text

    # ----------------------------------------------------------------------------------
    # ファイルアップロード

    @decoInstance.funcBase
    def files_input(
        self, value: str, file_path: str, by: str='xpath'):

        # アップロード場所の特定
        element = self.getElement(value=value, by=by)

        element_value =  element.get_attribute("value")

        # すでに入力されているものがあればクリア
        if element_value:
            self.logger.warning(f'すでに既存で入力されています: {element_value}')
            try:
                element.clear()
            except Exception:
                self.chrome.execute_script("arguments[0].value = '';", element)
        else:
            self.logger.info(f'既存で入力されているファイルPathはありません。')

        self.logger.debug(f"file_path: {file_path}")

        # ファイルPathを記入
        element.send_keys("\n".join(file_path))


    # ----------------------------------------------------------------------------------
    # 特定のフォルダにあるファイルをすべて取得してリストにする

    def _get_all_files_path_list(self, subDirName: str, subSubDirName):
        # photoのあるディレクトリ
        photo_dir = self.path.getInputPhotoDirPath(subDirName=subDirName, subSubDirName=subSubDirName)

        # input_photo内にあるすべてのファイルのフルパスをリスト化する
        all_photos_all_path_list = self._get_photos_all_path_list(photo_dir=photo_dir)
        if not all_photos_all_path_list:
            self.popup.popupCommentOnly(popupTitle=ErrorComment.PHOTO_TITLE.value, comment=ErrorComment.PHOTO_COMMENT.value.format(photo_dir))
        return all_photos_all_path_list


    # ----------------------------------------------------------------------------------
    # input_photo内にあるすべてのファイルのフルパスをリスト化する

    def _get_photos_all_path_list(self, photo_dir: str):
        dir_path = Path(photo_dir)
        all_photos_all_path_list = [str(file) for file in dir_path.rglob('*') if file.is_file()]
        self.logger.debug(f'all_photos_all_path_list: {all_photos_all_path_list}')
        return all_photos_all_path_list


    # ----------------------------------------------------------------------------------
    # Sortするようにしてアップロードする順番を決める
    # 最後の数字を拾ってSortする

    def _list_sort_photo_data(self, all_photos_all_path_list: List[str]):
        # 有効な拡張子を定義
        valid_extensions = {".jpeg", ".jpg", ".png"}

        # 拡張子をフィルタリング
        filtered_list = [
            path for path in all_photos_all_path_list
            if any(path.lower().endswith(ext) for ext in valid_extensions)
        ]
        self.logger.debug(f'filtered_list: {filtered_list}')

        # 数値でソート
        sorted_list = sorted(filtered_list, key=self._extract_num)

        self.logger.debug(f'sorted_list: {sorted_list}')
        return sorted_list


    # ----------------------------------------------------------------------------------
    # 文字列から数値を抽出する→A_Folder1→１

    def _extract_num(self, file_path: str):
        file_name = os.path.basename(file_path)
        match = re.search(r'\d+', file_name)   # ファイル名から数字を抽出
        extract_num = int(match.group()) if match else float('inf')  # 数値がない場合は優先度低めに設定
        self.logger.debug(f'extract_num: {extract_num}')
        return extract_num


    # ----------------------------------------------------------------------------------
    # クリックしてから入力

    @decoInstance.funcBase
    def clickClearInput(self, value: str, inputText: str, by: str = "xpath"):
        self.clickWait.canWaitClick(chrome=self.chrome, by=by, value=value, timeout=3)
        element = self.getElement(by=by, value=value)
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
        element = self.getElement(by=by, value=value)
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
        element = self.getElement(by=by, value=value)
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

    def recaptcha_click_element(
        self, by: str, value: str, home_url: str, check_element_by: str, check_element_value: str, max_retry: int = 40, delay: int = 5
    ):
        self.clickWait.canWaitClick(chrome=self.chrome, by=by, value=value, timeout=3)
        element = self.getElement(by=by, value=value)

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
    # 絞り込んだ要素にあるテキストを取得

    @decoInstance.funcBase
    def _get_text(self, element: WebElement):
        return element.text.strip()  # 前後の余白を除去

    # ----------------------------------------------------------------------------------

    @decoInstance.funcBase
    def getImageUrl(self, by: str, value: str):
        element = self.getElement(by=by, value=value)
        return element.get_attribute("src")

    # ----------------------------------------------------------------------------------

    def _getItemsList(self, by: str, value: str):
        itemElements = self.getElement(by=by, value=value)
        itemsText = itemElements.text
        itemsList = itemsText.split(", ")
        return itemsList

    # ----------------------------------------------------------------------------------
    # NGWordを除外リスト

    def textCleaner(self, textList: List, minLen: int = 12):
        ngWords = NGWordList.ngWords.value
        filterWordsList = self.textManager.filterWords(
            textList=textList, ngWords=ngWords
        )

        self.logger.warning(f"filterWordsList: {filterWordsList}\ntextList: {textList}")
        filterWordsListNum = len(filterWordsList)

        print(f"filterWordsListNum: {filterWordsListNum}")
        if minLen >= filterWordsListNum:
            newTextList = textList.split("，")
            print(f"newTextList: {newTextList}")
            return newTextList

        return filterWordsList

    # ----------------------------------------------------------------------------------

    def _getAddress(self, by: str, value: str):
        fullAddress = self.getElement(by=by, value=value)
        addressList = Address.addressList.value

        for address in addressList:
            if fullAddress.startswith(address):
                return address

    # ----------------------------------------------------------------------------------
    # 辞書dataの初期化

    def _initDict(self, name: str):  # -> dict[str, dict]:
        return {name: {}}

    # ----------------------------------------------------------------------------------
    # サブ辞書の中身を入れ込む

    def updateSubDict(
        self, dictBox: Dict[str, Dict[str, Any]], name: str, inputDict: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        dictBox[name].update(inputDict)
        return dictBox

    # ----------------------------------------------------------------------------------
    # 特定の値だった場合にNoneを返す

    def _returnNoneIfValue(self, value: Any, ifValueList: List):
        for ifValue in ifValueList:
            if value == ifValue:
                return None
            else:
                return value

    # ----------------------------------------------------------------------------------
    # 要素を繰り返し取得してリストにする
    # conditions=[(by, value), (otherBy, otherValue)]のようにtupleのリストを返す

    def _getElementList(self, conditions: List[Tuple[str, str]], ifValueList: List):
        elementList = []
        for by, value in conditions:
            element = self.getElement(by=by, value=value)
            # 特定のリストは除外する
            element = self._returnNoneIfValue(value=element, ifValueList=ifValueList)
            elementList.append(element)
        return elementList

    # ----------------------------------------------------------------------------------
    # 広告、検索画面などを検知して消去する

    def closePopup(self, by: str, value: str):
        element = self.clickWait.canWaitClick(chrome=self.chrome, by=by, value=value)
        if element:
            self.clickElement(by=by, value=value)
            self.logger.info(f"不要物を除去: {element}")
        else:
            self.logger.info(f"modalは出力されませんでした。")
            return

    # ----------------------------------------------------------------------------------
    # クリックした新しいページに切り替え

    def clickMove(self, by: str, value: str):
        self.clickElement(by=by, value=value)
        allHandles = self.chrome.window_handles  # すべてのWindowハンドルを取得
        self.chrome.switch_to.window(allHandles[-1])  # 元々のWindowはallHandles[0]
        return self.logger.info(
            f"クリックした新しいページタイトル「{self.chrome.title}」"
        )

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





# ----------------------------------------------------------------------------------
# 取得した要素から選択する

    def _select_element(self, value: str, select_value: str, by: str='xpath', on_text: bool=False):
        try:
            # プルダウン系の要素を選択
            element = self.getElement(by=by, value=value)
            self.logger.debug(f'element: {element}')
            self.logger.debug(f'element.text: \n{element.text}')
            self.logger.debug(f'element: {element.get_attribute("value")}')

            # element.click()

            # Selectで要素を定義
            select_element = Select(element)

            html_log = element.get_attribute('outerHTML')
            self.logger.debug(f'HTML: \n{html_log}')
            option_list = select_element.options
            op_text_list = [op.get_attribute('textContent') for op in option_list]
            self.logger.debug(f'選択肢の一覧: \n{op_text_list}')

            if on_text:
                # select_element.select_by_visible_text(select_value)
                for option in option_list:
                    if option.get_attribute('value') == select_value:
                        option.click()
                        break
            else:
                # 要素を特定する
                # select_element.select_by_value(select_value)
                for option in option_list:
                    if option.get_attribute('value') == select_value:
                        option.click()
                        # JSでvalueを設定してからchangeイベントを発火
                        self.chrome.execute_script("""
                            const select = arguments[0];
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                        """, element)
                        break

            selected_option = select_element.first_selected_option
            self.logger.debug(f'現在選択中の値: {selected_option.text}')

        except ElementNotInteractableException:
            self.logger.debug(f"⚠️ 要素は見つかったけど、操作できません！: {element}")
            html_log = element.get_attribute('outerHTML')
            self.logger.debug(f"⚠️ 要素のHTML: \n{html_log}")
            raise

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} _select_element 取得した要素を選択中にエラーが発生: {e}')

    # ----------------------------------------------------------------------------------
    # 特定の要素が無効化されているか確認


    def _disable_element_check(self, value: str, by: str='xpath'):
        try:
            disable_element = self.getElement(by=by, value=value)

            if disable_element:
                return True
        except NoSuchElementException as e:
            self.logger.debug(f'無効化されてない')
            return False



    # ----------------------------------------------------------------------------------
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


    def _enter_tab_chains(self):
        actions = ActionChains(self.chrome)
        actions.send_keys(Keys.TAB).pause(0.5).send_keys(Keys.ENTER).perform()
