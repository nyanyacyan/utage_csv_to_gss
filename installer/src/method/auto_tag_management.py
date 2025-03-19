# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/multi_site_post_flow/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from typing import Dict
from datetime import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from urllib3.exceptions import NewConnectionError
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.spreadsheet.spreadsheetRead import GetDataGSSAPI
from method.base.selenium.get_element import GetElement
from method.base.selenium.click_element import ClickElement
from method.base.decorators.decorators import Decorators
from method.base.utils.time_manager import TimeManager
from method.base.selenium.google_drive_download import GoogleDriveDownload
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.select_cell import GssSelectCell
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.base.utils.popup import Popup

# const
from method.const_element import GssInfo, LoginInfo, ErrCommentInfo, PopUpComment

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ

class TagManagementFlow:
    def __init__(self, chrome: WebDriver):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

        # インスタンス
        self.login = SingleSiteIDLogin(chrome=self.chrome)
        self.selenium = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.time_manager = TimeManager()
        self.get_element = GetElement(chrome=self.chrome)
        self.click_element = ClickElement(chrome=self.chrome)
        self.gss_read = GetDataGSSAPI()
        self.gss_write = GssWrite()
        self.drive_download = GoogleDriveDownload()
        self.select_cell = GssSelectCell()
        self.gss_check_err_write = GssCheckerErrWrite()
        self.popup = Popup()

        # const
        self.const_gss_info = GssInfo.LGRAM.value
        self.const_login_info = LoginInfo.LGRAM.value
        self.const_err_cmt_dict = ErrCommentInfo.LGRAM.value
        self.popup_cmt = PopUpComment.LGRAM.value

        self.const_post = Post.LGRAM.value
        self.const_tag_management = TagManagement.LGRAM.value

        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    ####################################################################################
    # ----------------------------------------------------------------------------------
    # ステップ配信flow

    def process(self, gss_info: Dict, err_datetime_cell: str, err_cmt_cell: str, max_count: int=3):
        retry_count = 0
        while retry_count < max_count:
            try:
                # タグ管理をクリック
                self.click_element.clickElement(value=self.const_tag_management["TAG_MANAGEMENT_BAR_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} タグ管理をクリック: 実施済み')
                self.selenium._random_sleep()

                # 未分類をクリック
                # self.click_element.clickElement(value=self.const_tag_management["UN_CATEGORIZE_BTN_VALUE"])
                # self.logger.warning(f'{self.__class__.__name__} 未分類をクリック: 実施済み')
                # self.selenium._random_sleep()

                # タグがあるかを確認
                try:
                    self.get_element.getElement(value=self.const_tag_management["EXITS_PROGRESS_TAG_VALUE"])
                    self.logger.info(f'「対応中」のタグはすでにあります。')
                    self.selenium._random_sleep()
                    return

                except NoSuchElementException:
                    self.logger.info(f'「対応中」のタグはないため新規作成します。')

                # ＋タグ新規作成をクリック
                self.click_element.clickElement(value=self.const_tag_management["CREATE_TAG_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} ＋タグ新規作成をクリック: 実施済み')
                self.selenium._random_sleep()

                # タグ管理名の入力（対応中）
                management_name = f"{self.const_tag_management['PROGRESS_TAG_VALUE']}"
                self.click_element.clickClearInput(value=self.const_tag_management["TAG_MANAGEMENT_NAME_VALUE"], inputText=management_name)
                # self.get_element._enter_tab_chains()  # タブキー→エンターキーを押す
                self.logger.warning(f'{self.__class__.__name__} タグ管理名の入力（対応中）: 実施済み')
                self.selenium._random_sleep()

                # 作成するをクリック
                self.click_element.clickElement(value=self.const_tag_management["CREATE_BTN_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} 作成するをクリック: 実施済み')
                self.selenium._random_sleep()

                # 保存するをクリック
                self.click_element.clickElement(value=self.const_tag_management["SAVE_BTN_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} 保存するをクリック: 実施済み')
                self.selenium._random_sleep()

                self.logger.info(f'{self.__class__.__name__} process: 実施済み')
                return

            except StaleElementReferenceException as e:
                self.logger.warning(f'{self.__class__.__name__} エラー発生、リトライ実施: {retry_count + 1}/{max_count} → {e}')
                time.sleep(1)  # 少し待って再取得
                retry_count += 1

            except NewConnectionError as e:
                self.logger.warning(f'{self.__class__.__name__} エラー発生、リトライ実施: {retry_count + 1}/{max_count} → {e}')
                time.sleep(1)  # 少し待って再取得
                retry_count += 1

            except Exception as e:
                self.logger.warning(f'{self.__class__.__name__} エラー発生、リトライ実施: {retry_count + 1}/{max_count} → {e}')
                time.sleep(1)  # 少し待って再取得
                retry_count += 1

                # エラータイムスタンプ
                self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp)

                # エラーコメント
                self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=error_comment)
                self.chrome.quit()
                raise

        # `max_count` に達した場合、エラーを記録
        self.logger.error(f'{self.__class__.__name__} 最大リトライ回数 {max_count} 回を超過。処理を中断')

        error_comment = f"【自動投稿】最大リトライ回数 {max_count} 回を超過"

        # スプレッドシートにエラーを記録
        self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp)
        self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=error_comment)

        self.chrome.quit()
        raise TimeoutError(f"最大リトライ回数 {max_count} 回を超過しました。")

    # ----------------------------------------------------------------------------------
