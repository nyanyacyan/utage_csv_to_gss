# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/LGRAM_auto_processer/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os
import concurrent.futures
from typing import Dict
from datetime import datetime

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.chrome import ChromeManager
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.spreadsheet.spreadsheetRead import GetDataGSSAPI
from method.base.selenium.get_element import GetElement
from method.base.decorators.decorators import Decorators
from method.base.utils.time_manager import TimeManager
from method.base.selenium.google_drive_download import GoogleDriveDownload
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.select_cell import GssSelectCell
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.utils.popup import Popup
from method.base.selenium.click_element import ClickElement
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException

# flow
from method.prepare_flow import PrepareFlow
from method.auto_post_flow import AutoPostFlow
from method.auto_tag_management import TagManagementFlow
from method.step_delivery_flow import StepDeliveryFlow
from method.auto_reply import AutoReplyFlow

# const
from method.const_element import GssInfo, LoginInfo, ErrCommentInfo, PopUpComment, Post

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ


class FlowProcess:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.time_manager = TimeManager()
        self.gss_read = GetDataGSSAPI()
        self.gss_write = GssWrite()
        self.drive_download = GoogleDriveDownload()
        self.select_cell = GssSelectCell()
        self.gss_check_err_write = GssCheckerErrWrite()
        self.popup = Popup()



        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # const
        self.const_gss_info = GssInfo.LGRAM.value
        self.const_login_info = LoginInfo.LGRAM.value
        self.const_err_cmt_dict = ErrCommentInfo.LGRAM.value
        self.popup_cmt = PopUpComment.LGRAM.value


    ####################################################################################
    # ----------------------------------------------------------------------------------
    # 各メソッドをまとめる

    def parallel_process(self, max_workers: int = 3):
        try:
            # スプシにアクセス（Worksheet指定）
            df = self.gss_read._get_df_gss_url(gss_info=self.const_gss_info)
            df_filtered = df[df["チェック"] == "TRUE"]

            self.logger.debug(f'DataFrame: {df_filtered.head()}')

            # 並列処理
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []

                for i, row in df_filtered.iterrows():
                    row_num = i + 1
                    get_gss_row_dict = row.to_dict()

                    # 完了通知column名
                    complete_datetime_col_name = self.const_gss_info["POST_COMPLETE_DATE"]

                    # エラーcolumn名
                    err_datetime_col_name = self.const_gss_info["ERROR_DATETIME"]
                    err_cmt_col_name = self.const_gss_info["ERROR_COMMENT"]

                    complete_cell = self.select_cell.get_cell_address(
                        gss_row_dict=get_gss_row_dict,
                        col_name=complete_datetime_col_name,
                        row_num=row_num,
                    )

                    err_datetime_cell = self.select_cell.get_cell_address(
                        gss_row_dict=get_gss_row_dict,
                        col_name=err_datetime_col_name,
                        row_num=row_num,
                    )
                    err_cmt_cell = self.select_cell.get_cell_address(
                        gss_row_dict=get_gss_row_dict,
                        col_name=err_cmt_col_name,
                        row_num=row_num,
                    )

                    # `SingleProcess` を **新しく作成**
                    single_flow_instance = SingleProcess()

                    future = executor.submit(
                        single_flow_instance._single_process,
                        gss_row_data=get_gss_row_dict,
                        gss_info=self.const_gss_info,
                        complete_cell=complete_cell,
                        err_datetime_cell=err_datetime_cell,
                        err_cmt_cell=err_cmt_cell,
                        login_info=self.const_login_info,
                    )

                    futures.append(future)

                concurrent.futures.wait(futures)

            self.popup.popupCommentOnly(
                popupTitle=self.popup_cmt["ALL_COMPLETE_TITLE"],
                comment=self.popup_cmt["ALL_COMPLETE_COMMENT"],
            )

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラーが発生: {e}')



    # ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ

class SingleProcess:
    def __init__(self):
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # const
        self.const_gss_info = GssInfo.LGRAM.value
        self.const_login_info = LoginInfo.LGRAM.value
        self.const_post = Post.LGRAM.value
        self.const_err_cmt_dict = ErrCommentInfo.LGRAM.value
        self.popup_cmt = PopUpComment.LGRAM.value

# **********************************************************************************
    # ----------------------------------------------------------------------------------


    def _single_process(self, gss_row_data: Dict, gss_info: Dict, complete_cell: str, err_datetime_cell: str, err_cmt_cell: str, login_info: Dict):
        """ 各プロセスを実行する """

        # ✅ Chrome の起動をここで行う
        self.chromeManager = ChromeManager()
        self.chrome = self.chromeManager.flowSetupChrome()

        try:
            # インスタンスの作成 (chrome を引数に渡す)
            self.login = SingleSiteIDLogin(chrome=self.chrome)
            self.random_sleep = SeleniumBasicOperations(chrome=self.chrome)
            self.get_element = GetElement(chrome=self.chrome)
            self.selenium = SeleniumBasicOperations(chrome=self.chrome)
            self.gss_read = GetDataGSSAPI()
            self.gss_write = GssWrite()
            self.drive_download = GoogleDriveDownload()
            self.select_cell = GssSelectCell()
            self.gss_check_err_write = GssCheckerErrWrite()
            self.popup = Popup()
            self.click_element = ClickElement(chrome=self.chrome)

            # 各Flow
            self.prepare_flow = PrepareFlow(chrome=self.chrome)
            self.auto_post_flow = AutoPostFlow(chrome=self.chrome)
            self.tag_management_flow = TagManagementFlow(chrome=self.chrome)
            self.step_delivery_flow = StepDeliveryFlow(chrome=self.chrome)
            self.auto_reply_flow = AutoReplyFlow(self.chrome)

            # ✅ ここから通常の処理
            image_path, movie_path = self.prepare_flow.prepare_process(
                gss_row_data=gss_row_data, gss_info=gss_info, err_datetime_cell=err_datetime_cell, err_cmt_cell=err_cmt_cell
            )

            self.login.flow_login_id_input_gui(
                login_info=login_info, id_text=gss_row_data[self.const_gss_info["ID"]], pass_text=gss_row_data[self.const_gss_info["PASSWORD"]], gss_info=gss_info, err_datetime_cell=err_datetime_cell, err_cmt_cell=err_cmt_cell
            )

            # アカウントをクリック
            self.click_element.clickElement( by=self.const_post["SELECT_ACCOUNT_BY"], value=self.const_post["SELECT_ACCOUNT_VALUE"] )
            self.logger.warning(f'{self.__class__.__name__} アカウント名をクリック: 実施済み')
            self.selenium._random_sleep(3, 5)

            try:
                # Facebookのアカウント確認がはいったことを想定
                facebook_login = self.get_element.getElement(value=self.const_post["IF_FACEBOOK_VALUE"])

                if facebook_login:
                    facebook_login.click()
                    facebook_comment = "Facebookのログインができておりません。"
                    self.logger.error(f'{self.__class__.__name__} facebook_comment: {facebook_comment}')
                    # エラータイムスタンプ
                    self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp)

                    # エラーコメント
                    self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=facebook_comment)
                    raise Exception(facebook_comment)

            except ElementNotInteractableException:
                self.logger.info(f'Facebookはログイン状態')

            # 自動投稿
            self.auto_post_flow.process(gss_row_data, gss_info, err_datetime_cell, err_cmt_cell)
            self.tag_management_flow.process(gss_info, err_datetime_cell, err_cmt_cell)

            # ステップ配信
            self.step_delivery_flow.first_process(gss_row_data, gss_info, err_datetime_cell, err_cmt_cell)
            self.step_delivery_flow.second_process(gss_row_data, gss_info, err_datetime_cell, err_cmt_cell)
            self.step_delivery_flow.third_process(gss_row_data, gss_info, err_datetime_cell, err_cmt_cell)

            # 自動応答
            result_bool = self.auto_reply_flow.process(gss_row_data, gss_info, err_datetime_cell, err_cmt_cell)

            if result_bool:
                self.gss_write.write_data_by_url(gss_info, complete_cell, input_data=str(self.timestamp))

            self.logger.info(f'{gss_row_data[self.const_gss_info["NAME"]]}: 処理完了')

        except TimeoutError:
            timeout_comment = "ログインでreCAPTCHA処理にが長引いてしまったためエラー"
            self.logger.error(f'{self.__class__.__name__} {timeout_comment}')
            # エラータイムスタンプ
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp)

            # エラーコメント
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=timeout_comment)

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} エラー: {e}')

        finally:
            self._delete_file(image_path)
            self._delete_file(movie_path)
            # ✅ Chrome を終了
            self.chrome.quit()


    # ----------------------------------------------------------------------------------

    def _delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
            self.logger.info(f'指定のファイルの削除を実施: {file_path}')

        else:
            self.logger.error(f'{self.__class__.__name__} ファイルが存在しません: {file_path}')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# テスト実施

if __name__ == "__main__":

    test_flow = FlowProcess()
    # 引数入力
    test_flow.parallel_process()
