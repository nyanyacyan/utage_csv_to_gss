# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/multi_site_post_flow/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from typing import Dict
from datetime import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.utils.path import BaseToPath
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
from method.const_element import GssInfo, LoginInfo, ErrCommentInfo, PopUpComment, Post

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ

class AutoPostFlow:
    def __init__(self, chrome: WebDriver):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

        # インスタンス
        self.login = SingleSiteIDLogin(chrome=self.chrome)
        self.random_sleep = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.click_element = ClickElement(chrome=self.chrome)
        self.time_manager = TimeManager()
        self.selenium = SeleniumBasicOperations(chrome=self.chrome)
        self.gss_read = GetDataGSSAPI()
        self.gss_write = GssWrite()
        self.drive_download = GoogleDriveDownload()
        self.select_cell = GssSelectCell()
        self.gss_check_err_write = GssCheckerErrWrite()
        self.popup = Popup()
        self.path = BaseToPath()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # const
        self.const_gss_info = GssInfo.LGRAM.value
        self.const_login_info = LoginInfo.LGRAM.value
        self.const_err_cmt_dict = ErrCommentInfo.LGRAM.value
        self.popup_cmt = PopUpComment.LGRAM.value
        self.const_post = Post.LGRAM.value


    ####################################################################################


    def process(self, gss_row_data, gss_info: Dict, err_datetime_cell: str, err_cmt_cell: str, max_count: int= 3):
        retry_count = 0
        while retry_count < max_count:
            try:
                # 投稿機能を開く
                self.click_element.clickElement(value=self.const_post["POST_EXTENSIONS_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} 投稿機能を開く: 実施済み')
                self.selenium._random_sleep()

                # 投稿作成をクリック
                self.click_element.clickElement(value=self.const_post["POST_CREATE_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} 投稿作成をクリック: 実施済み')
                self.selenium._random_sleep()

                # ＋投稿をクリック
                self.click_element.clickElement(value=self.const_post["PLUS_POST_CREATE_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} ＋投稿をクリック: 実施済み')
                self.selenium._random_sleep()

                # 管理名の入力（日付）
                self.click_element.clickClearInput(by=self.const_post["MANAGEMENT_NAME_BY"], value=self.const_post["MANAGEMENT_NAME_VALUE"], inputText=self.timestamp)
                self.get_element._enter_tab_chains()  # タブキー→エンターキーを押す
                self.logger.warning(f'{self.__class__.__name__} 管理名の入力（日付）: 実施済み')
                self.selenium._random_sleep()

                # リール投稿を選択
                self.click_element.clickElement(value=self.const_post["REEL_SELECT_BTN_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} リール投稿を選択: 実施済み')
                self.selenium._random_sleep()

                # 投稿編集へ進む
                self.click_element.clickElement(value=self.const_post["REEL_SELECT_POST_BTN_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} 投稿編集へ進む: 実施済み')
                self.selenium._random_sleep()

                # 動画挿入
                gss_name = gss_row_data[self.const_gss_info["NAME"]]
                reel_drive_url = gss_row_data[self.const_gss_info["REEL_URL"]]
                file_path = self.drive_download._create_download_file_path(gss_info=gss_info, drive_url=reel_drive_url, sub_dir_name=gss_name)
                file_input = self.chrome.find_element(By.CSS_SELECTOR, "input[type='file']")
                self.logger.debug(f'file_input: {file_input}')
                file_input.send_keys(str(file_path))
                self.logger.warning(f'{self.__class__.__name__} 動画挿入: 実施済み')
                self.selenium._random_sleep(7, 10)

                try:
                    WebDriverWait(self.chrome, 60).until( EC.presence_of_element_located((By.XPATH, self.const_post["IMAGE_SELECT_BTN_VALUE"])) )
                    self.logger.info(f'次の要素が確認できました。')

                except TimeoutException:
                    self.logger.error(f'{self.__class__.__name__} 次の要素が確認できませんでした。')
                    time.sleep(1)  # 少し待って再取得
                    retry_count += 1
                    continue

                # 画像を変更するをクリック
                self.click_element.clickElement(value=self.const_post["IMAGE_SELECT_BTN_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} 画像を変更するをクリック: 実施済み')
                self.selenium._random_sleep()

                # サムネイル画像を挿入
                gss_name = gss_row_data[self.const_gss_info["NAME"]]
                reel_drive_url = gss_row_data[self.const_gss_info["THUMBNAIL_URL"]]
                file_path = self.drive_download._create_download_file_path(gss_info=gss_info, drive_url=reel_drive_url, sub_dir_name=gss_name)
                file_input = self.chrome.find_element(By.CSS_SELECTOR, "input[type='file']")
                self.logger.debug(f'file_input: {file_input}')
                file_input.send_keys(str(file_path))
                self.logger.warning(f'{self.__class__.__name__} サムネイル画像を挿入: 実施済み')
                self.selenium._random_sleep()

                # 詳細設定へ進むをクリック
                self.click_element.clickElement(value=self.const_post["GO_SETTING_BTN_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} １つ目の詳細設定へ進むをクリック: 実施済み')
                self.selenium._random_sleep()

                # さらに詳細設定へ進むをクリック
                self.click_element.clickElement(value=self.const_post["RETURN_GO_SETTING_BTN_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} ２つ目の詳細設定へ進むをクリック: 実施済み')
                self.selenium._random_sleep()

                # 日時を入力
                date_data = gss_row_data[self.const_gss_info["RESERVE_DAY"]]
                fixed_date_data = "00" + date_data
                self.logger.debug(f'fixed_date_data: {fixed_date_data}')
                self.click_element.clickClearInput(value=self.const_post["DATE_INPUT_VALUE"], inputText=fixed_date_data)
                self.logger.warning(f'{self.__class__.__name__} 日時の入力: 実施済み')
                self.selenium._random_sleep()

                # 時間を入力
                time_data = gss_row_data[self.const_gss_info["RESERVE_TIME"]]
                time_data_input_field = self.chrome.find_element(By.XPATH, value=self.const_post["TIME_INPUT_VALUE"])
                time_data_input_field.send_keys(Keys.BACKSPACE * 5)
                time_data_input_field.send_keys(time_data)
                time_data_input_field.send_keys(Keys.TAB)
                self.logger.warning(f'{self.__class__.__name__} 時間の入力: 実施済み')
                self.selenium._random_sleep()

                # キャプションの入力
                caption_data = gss_row_data[self.const_gss_info["CAPTION"]]
                self.click_element.clickClearInput(value=self.const_post["CAPTION_INPUT_VALUE"], inputText=caption_data)
                self.logger.warning(f'{self.__class__.__name__} 設定内容を確認して投稿するをクリック: 実施済み')
                self.selenium._random_sleep()

                # 設定内容を確認して投稿するをクリック
                self.click_element.clickElement(value=self.const_post["GO_CHECK_BTN_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} 設定内容を確認して投稿するをクリック: 実施済み')
                self.selenium._random_sleep()

                # この内容で投稿するをクリック
                self.click_element.clickElement(value=self.const_post["GO_POST_BTN_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} この内容で投稿する: 実施済み')
                self.selenium._random_sleep()
                return

            except (StaleElementReferenceException, NoSuchElementException) as e:
                self.logger.critical(f'{self.__class__.__name__} エラー発生、リトライ実施: {retry_count + 1}/{max_count} → {e}')
                time.sleep(1)  # 少し待って再取得
                retry_count += 1


            except Exception as e:
                self.logger.error(f'{self.__class__.__name__} 処理中にエラーが発生: {e}')
                error_comment = f"【自動投稿】処理中にエラーが発生: {e}"

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


    def _click_element_facebook_guard(self, value: str, by: str ="xpath"):
        try:
            self.click_element.clickElement(by=by, value=value)
            self.selenium._random_sleep()

        except NoSuchElementException:
            self.logger.warning(f'{self.__class__.__name__} 対象の要素が見つかりません')

            # facebookのPOPUPを削除
            self.click_element.clickElement(by=self.const_post["FACEBOOK_CLOSE_BY"], value=self.const_post["FACEBOOK_CLOSE_VALUE"])
            self.selenium._random_sleep(2, 5)

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラーが発生: {e}')

            # facebookのPOPUPを削除
            self.click_element.clickElement(by=self.const_post["FACEBOOK_CLOSE_BY"], value=self.const_post["FACEBOOK_CLOSE_VALUE"])
            self.selenium._random_sleep(2, 5)

    ####################################################################################
    # TODO ファイルを選択できるようにする
    # 指定の拡張子を入力できたらその後削除する

    def _extract_reel_movie_file(self, extension_folder_name: str, sub_dir_name: str):
        save_path = self.path._get_input_sub_sub_extension_folder(sub_dir_name=sub_dir_name, extension_folder_name=extension_folder_name)
        self.logger.debug(f'save_path: {save_path}')


        video_files = list(save_path.glob("*.mp4")) + list(save_path.glob("*.mov"))
        if len(video_files) == 0:
            # ここにエラーがスプシに反映するようにする
            raise FileNotFoundError(f"❌ {save_path} に動画ファイルが見つかりませんでした。")

        elif len(video_files) > 1:
            raise ValueError(f"❌ {save_path} 複数のファイルがみつかりました。")

        return video_files[0]

    # ----------------------------------------------------------------------------------
