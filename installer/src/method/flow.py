# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/LGRAM_auto_processer/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os
import pandas as pd
import concurrent.futures
from typing import Dict
from datetime import datetime
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException

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
from method.base.utils.file_move import FileMove

# flow
from method.prepare_flow import PrepareFlow
from method.auto_post_flow import AutoPostFlow
from method.auto_tag_management import TagManagementFlow
from method.step_delivery_flow import StepDeliveryFlow
from method.auto_reply import AutoReplyFlow

# const
from method.const_element import GssInfo, LoginInfo, ErrCommentInfo, PopUpComment, Element

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

            # 上記URLからWorksheetを取得
            existing_titles = self.gss_read._sort_worksheet(gss_info=self.const_gss_info)

            # 取得シートのnameの全リスト出力
            name_list = df_filtered[self.const_gss_info["NAME"]].tolist()

            # 現Worksheetに取得シートのnameに記載あるリストと突合
            diff_name_list = [name for name in name_list if name not in existing_titles]
            self.logger.info(f'作成するWorksheetのリスト: {diff_name_list}')

            # なければ作成→ABCのcolumnは指定
            if diff_name_list:
                for name in diff_name_list:
                    self.gss_write._create_worksheet_add_col(gss_info=self.const_gss_info, title_name=name)

            else:
                self.logger.info('追加するWorksheetはありません')

            all_worksheet = existing_titles + diff_name_list

            self.logger.info(f'全Worksheetリスト: {all_worksheet}')

            # 並列処理
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []

                for i, row in df_filtered.iterrows():
                    row_num = i + 1
                    get_gss_row_dict = row.to_dict()  # ここにgss情報

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
        self.timestamp = datetime.now()
        self.date_only_stamp = self.timestamp.date()

        # const
        self.const_gss_info = GssInfo.UTAGE.value
        self.const_login_info = LoginInfo.UTAGE.value
        self.const_element = Element.UTAGE.value
        self.const_err_cmt_dict = ErrCommentInfo.UTAGE.value
        self.popup_cmt = PopUpComment.UTAGE.value

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
            self.file_move = FileMove()


            # URLのアクセス→ID入力→Passの入力→ログイン
            self.login.flow_login_id_input_gui( login_info=login_info, id_text=gss_row_data[self.const_gss_info["ID"]], pass_text=gss_row_data[self.const_gss_info["PASSWORD"]], gss_info=gss_info, err_datetime_cell=err_datetime_cell, err_cmt_cell=err_cmt_cell )

            # 【絞り込み条件】指定した条件に該当する読者を表示をクリック
            self.click_element.clickElement(value=self.const_element["MATCH_RULES"])
            self.logger.warning(f'{self.__class__.__name__} 指定した条件に該当する読者を表示をクリック: 実施済み')
            self.selenium._random_sleep()

            # ドロップダウン → 配信基準日時（日付）→
            self.get_element._select_element(by=self.const_element["MATCH_CHOICE_BY"], value=self.const_element["MATCH_CHOICE_VOL"], select_value=self.const_element["DELIVERY_SETTING_SELECT_OPTION_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 開始/再開を選択（ドロップダウン）: 実施済み')
            self.selenium._random_sleep()

            # ドロップダウン 次と完全一致
            self.get_element._select_element(by=self.const_element["DELIVERY_SETTING_SELECT_BY"], value=self.const_auto_reply["DELIVERY_SETTING_SELECT_VALUE"], select_value=self.const_element["MATCH_CHOICE_SELECT_VOL"])
            self.logger.warning(f'{self.__class__.__name__} 開始/再開を選択（ドロップダウン）: 実施済み')
            self.selenium._random_sleep()

            # 前日を入力 →
            date_data = self.date_only_stamp
            fixed_date_data = "00" + date_data
            self.logger.debug(f'fixed_date_data: {fixed_date_data}')
            self.click_element.clickClearInput(value=self.const_element["DATE_INPUT_VOL"], inputText=fixed_date_data)
            self.logger.warning(f'{self.__class__.__name__} 日時の入力: 実施済み')
            self.selenium._random_sleep()

            # 絞り込みをクリック →
            self.click_element.clickElement(value=self.const_element["SORTING_VOL"])
            self.logger.warning(f'{self.__class__.__name__} 絞り込みをクリック: 実施済み')
            self.selenium._random_sleep()

            # CSV出力をクリック →
            self.click_element.clickElement(value=self.const_element["CSV_OUTPUT_VOL"])
            self.logger.warning(f'{self.__class__.__name__} CSV出力をクリック: 実施済み')
            self.selenium._random_sleep()

            # CSV移動
            csv_path = self.file_move.move_csv_dl_to_inputDir(sub_dir_name=self.const_element["CSV_OUTPUT_VOL"], file_name=gss_row_data["NAME"], extension=self.const_element["CSV_OUTPUT_VOL"])

            # CSVの読み込み
            download_csv_df = pd.read_csv(csv_path)
            self.logger.debug(f'ダウンロードしたCSVのdf: {download_csv_df.head()}')
            downloads_names_list = download_csv_df[self.const_gss_info["NAME"]]

            # GSSへアクセス→gss_row_dataにあるURLへアクセス
            gss_df = self.gss_read._get_gss_df_to_gui(gui_info=self.const_gss_info, sheet_url=self.const_gss_info["SHEET_URL"], worksheet_name=self.const_gss_info["NAME"])
            gss_names_list = gss_df[self.const_gss_info["NAME"]]

            # 対象のWorksheetから友達IDのリスト作成
            diff_name_list = [name for name in downloads_names_list if name not in gss_names_list]

            # CSVファイルから友達IDのリストを生成

            # 既存データとCSV友達IDのリスト突合→差異を抽出

                # LINE友達IDの入力

                # LINE登録名を入力

                # 登録日にタイムスタンプを入力



            # 実施を成功欄に日付を書込をする
            if result_bool:
                self.gss_write.write_data_by_url(gss_info, complete_cell, input_data=str(self.timestamp))

            self.logger.info(f'{gss_row_data[self.const_gss_info["NAME"]]}: 処理完了')

        except TimeoutError:
            timeout_comment = "タイムエラー：ログインに失敗している可能性があります。"
            self.logger.error(f'{self.__class__.__name__} {timeout_comment}')
            # エラータイムスタンプ
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp)

            # エラーコメント
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=timeout_comment)

        except Exception as e:
            timeout_comment = "ログインでreCAPTCHA処理にが長引いてしまったためエラー"
            self.logger.error(f'{self.__class__.__name__} {timeout_comment}')
            # エラータイムスタンプ
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp)

            # エラーコメント
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=timeout_comment)

        finally:
            self._delete_file(image_path)  # CSVファイルを消去

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
