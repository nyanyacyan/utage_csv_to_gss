# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/utage_csv_to_gss/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/utage_csv_to_drive/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, time, chardet
import pandas as pd
import concurrent.futures
from typing import Dict
from datetime import datetime, date, timedelta
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.chrome import ChromeManager, UCChromeManager
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
        self.const_gss_info = GssInfo.UTAGE.value
        self.const_login_info = LoginInfo.UTAGE.value
        self.const_err_cmt_dict = ErrCommentInfo.UTAGE.value
        self.popup_cmt = PopUpComment.UTAGE.value


    ####################################################################################
    # ----------------------------------------------------------------------------------
    # 各メソッドをまとめる

    def parallel_process(self, max_workers: int = 1):
        try:
            # スプシにアクセス（Worksheet指定）
            df = self.gss_read._get_df_gss_url(gss_info=self.const_gss_info)
            df_filtered = df[df["チェック"] == "TRUE"]

            self.logger.debug(f'DataFrame: {df_filtered.head()}')

            # 上記URLからWorksheetを取得
            existing_titles = self.gss_read._get_all_worksheet(gss_info=self.const_gss_info)

            # 取得シートのnameの全リスト出力
            name_list = df_filtered[self.const_gss_info["NAME"]].tolist()
            self.logger.debug(f'name_list: {name_list}')

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

                    complete_cell = self.select_cell.get_cell_address( gss_row_dict=get_gss_row_dict, col_name=complete_datetime_col_name, row_num=row_num, )

                    err_datetime_cell = self.select_cell.get_cell_address( gss_row_dict=get_gss_row_dict, col_name=err_datetime_col_name, row_num=row_num, )
                    err_cmt_cell = self.select_cell.get_cell_address( gss_row_dict=get_gss_row_dict, col_name=err_cmt_col_name, row_num=row_num, )

                    # `SingleProcess` を **新しく作成**
                    single_flow_instance = SingleProcess()

                    future = executor.submit( single_flow_instance._single_process, gss_row_data=get_gss_row_dict, gss_info=self.const_gss_info, complete_cell=complete_cell, err_datetime_cell=err_datetime_cell, err_cmt_cell=err_cmt_cell, login_info=self.const_login_info, )

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
        self.timestamp_two = self.timestamp.strftime("%Y-%m-%d %H:%M")
        self.date_only_stamp = self.timestamp.date().strftime("%m月%d日")

        # const
        self.const_gss_info = GssInfo.UTAGE.value
        self.const_login_info = LoginInfo.UTAGE.value
        self.const_element = Element.UTAGE.value
        self.const_err_cmt_dict = ErrCommentInfo.UTAGE.value
        self.popup_cmt = PopUpComment.UTAGE.value

# **********************************************************************************
    # ----------------------------------------------------------------------------------


    def _single_process(self, gss_row_data: Dict, gss_info: Dict, complete_cell: str, err_datetime_cell: str, err_cmt_cell: str, login_info: Dict, max_retry: int = 3):
        """ 各プロセスを実行する """
        for retry in range(max_retry):
            try:
                # ✅ Chrome の起動をここで行う
                self.chromeManager = ChromeManager()
                self.chrome = self.chromeManager.flowSetupChrome()

                self.chrome.execute_cdp_cmd( "Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); """ }, )


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
                self.login.flow_login_id_input_url( login_info=login_info, login_url=gss_row_data[self.const_gss_info["URL"]], id_text=gss_row_data[self.const_gss_info["ID"]], pass_text=gss_row_data[self.const_gss_info["PASSWORD"]], gss_info=gss_info, err_datetime_cell=err_datetime_cell, err_cmt_cell=err_cmt_cell )

                # 【絞り込み条件】指定した条件に該当する読者を表示をクリック
                self.click_element.clickElement(value=self.const_element["MATCH_RULES_VOL"])
                self.logger.warning(f'{self.__class__.__name__} 指定した条件に該当する読者を表示をクリック: 実施済み')
                self.selenium._random_sleep()


                self.get_element.unlockDisplayNone()

                # ドロップダウン → 配信基準日時（日付）→
                self.get_element._select_element(by=self.const_element["MATCH_CHOICE_BY"], value=self.const_element["MATCH_CHOICE_VOL"], select_value=self.const_element["MATCH_CHOICE_SELECT_VOL"])
                self.logger.warning(f'{self.__class__.__name__} 配信基準日時（日付）: 実施済み')
                self.selenium._random_sleep()

                # ドロップダウン 次と完全一致
                self.get_element._select_element(by=self.const_element["DELIVERY_SETTING_SELECT_BY"], value=self.const_element["DELIVERY_SETTING_SELECT_VALUE"], select_value=self.const_element["SETTING_SELECT_VALUE"])
                self.logger.warning(f'{self.__class__.__name__} 次と完全一致（ドロップダウン）: 実施済み')
                self.selenium._random_sleep()

                # # 絞り込みをクリック →
                self.click_element.clickElement(value=self.const_element["SORTING_VOL"])
                self.logger.warning(f'{self.__class__.__name__} 絞り込みをクリック: 実施済み')
                self.selenium._random_sleep()

                # 前日を入力
                today = date.today()
                yesterday = today - timedelta(days=1)
                self.logger.debug(f'date_data: {yesterday}')
                fixed_yesterday_data = "00" + str(yesterday)
                self.logger.debug(f'fixed_date_data: {fixed_yesterday_data}')
                self.click_element.clickClearInput(value=self.const_element["DATE_INPUT_VOL"], inputText=fixed_yesterday_data)
                self.logger.warning(f'{self.__class__.__name__} 日時の入力: 実施済み')
                self.selenium._random_sleep()
                break  # 成功したらループ抜ける

            except ElementNotInteractableException:
                gss_url_error_comment = self.const_err_cmt_dict["GSS_URL_ERROR"]
                self.logger.error(gss_url_error_comment)

                # エラータイムスタンプ
                self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp_two)
                # エラーコメント
                self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=gss_url_error_comment)
                return


            except NoSuchElementException as e:
                self.logger.warning(f'{self.__class__.__name__} ドロップダウンの選択に失敗: {e}')
                self.chrome.quit()
                self.logger.warning(f'{self.__class__.__name__} Chromeを終了')
                self.logger.warning(f'{self.__class__.__name__} リトライ: {retry + 1}/{max_retry}')  # リトライのためにChromeを再起動
                self.selenium._random_sleep()
                if retry == max_retry - 1:
                    self.logger.error(f'{self.__class__.__name__} 最大リトライ回数に達しました: {e}')
                    raise

        try:
            # 絞り込みをクリック →
            self.click_element.clickElement(value=self.const_element["SORTING_VOL"])
            self.logger.warning(f'{self.__class__.__name__} 絞り込みをクリック: 実施済み')
            self.selenium._random_sleep()

            # CSV出力をクリック →
            self.click_element.clickElement(value=self.const_element["CSV_OUTPUT_VOL"])
            self.logger.warning(f'{self.__class__.__name__} CSV出力をクリック: 実施済み')
            self.selenium._random_sleep()

            # CSV移動
            csv_path = self.file_move.move_csv_dl_to_inputDir(sub_dir_name=gss_row_data[self.const_gss_info["NAME"]], file_name_head=self.const_element["CSV_FILE_NAME"], extension=self.const_element["CSV_EXTENSION"])


            # CSVの読み込み
            download_csv_df = self._read_csv_with_encoding(file_path=csv_path)
            downloads_names_list = download_csv_df[self.const_gss_info["LINE_FRIEND_ID"]].tolist()
            self.logger.debug(f'downloads_names_list: {downloads_names_list}')

            # GSSへアクセス→gss_row_dataにあるURLへアクセス
            worksheet_name = gss_row_data[self.const_gss_info["NAME"]]
            self.logger.debug(f'worksheet_name: {worksheet_name}')
            gss_df = self.gss_read._get_gss_df_to_gui(gui_info=self.const_gss_info, sheet_url=self.const_gss_info["SHEET_URL"], worksheet_name=worksheet_name)
            if gss_df.empty:
                self.logger.info("対象のスプレッドシートは空です。全データを書き込み対象とします。")

                diff_name_list = downloads_names_list
                none_row_num = 1  # ヘッダー行を除いた次の行
            else:
                gss_names_list = gss_df[self.const_gss_info["LINE_FRIEND_ID"]].tolist()
                self.logger.debug(f'gss_names_list: \n{gss_names_list}')

                # CSVと既存との付け合せを行い差異リストを生成
                diff_name_list = [name for name in downloads_names_list if name not in gss_names_list]
                self.logger.debug(f'diff_name_list: {diff_name_list}')

                # 空白の行数
                none_row_num = self.gss_read._get_input_row_num(df=gss_df)
                self.logger.debug(f'none_row_num: {none_row_num}')

            # データフレームをフィルターかける（書き込むデータ飲みにする）
            df_row_filtered = download_csv_df[download_csv_df[self.const_gss_info["LINE_FRIEND_ID"]].isin(diff_name_list)]
            df_filtered = df_row_filtered[self.const_gss_info["CHOICE_COL"]]
            self.logger.debug(f'必要な情報だけのDataFrame: {df_filtered.head()}')

            if not df_filtered.empty:
                # 行ごとに処理
                for i, row in df_filtered.iterrows():
                    row_num = i + none_row_num
                    self.logger.debug(f'row_num: {row_num}')
                    get_gss_row_dict = row.to_dict()

                    # LINE友達IDのcell
                    friend_id_cell = self.select_cell.get_cell_address( gss_row_dict=get_gss_row_dict, col_name=self.const_gss_info["LINE_FRIEND_ID"], row_num=row_num, )

                    # LINE登録名のcell
                    line_name_cell = self.select_cell.get_cell_address( gss_row_dict=get_gss_row_dict, col_name=self.const_gss_info["LINE_NAME"], row_num=row_num, )

                    # 登録日にタイムスタンプのcell → Cにする → col_num=3
                    date_cell = self.select_cell.get_cell_address_add_col( col_num=3, col_name=self.const_gss_info["SIGN_UP_DATE"], row_num=row_num, )

                    # LINE友達IDの入力
                    self.gss_write.write_gss_base_cell_address(gss_info=self.const_gss_info, sheet_url=self.const_gss_info["SHEET_URL"], worksheet_name=worksheet_name, cell_address=friend_id_cell, input_value=get_gss_row_dict[self.const_gss_info["LINE_FRIEND_ID"]])
                    time.sleep(1)

                    # LINE登録名を入力
                    self.gss_write.write_gss_base_cell_address(gss_info=self.const_gss_info, sheet_url=self.const_gss_info["SHEET_URL"], worksheet_name=worksheet_name, cell_address=line_name_cell, input_value=get_gss_row_dict[self.const_gss_info["LINE_NAME"]])
                    time.sleep(1)

                    # 登録日にタイムスタンプを入力→C
                    self.logger.debug(f'date_cell: {date_cell}')
                    self.logger.debug(f'self.date_only_stamp: {self.date_only_stamp}')
                    self.gss_write.write_gss_base_cell_address(gss_info=self.const_gss_info, sheet_url=self.const_gss_info["SHEET_URL"], worksheet_name=worksheet_name, cell_address=date_cell, input_value=self.date_only_stamp)
                    time.sleep(1)

                    self.logger.info(f'LINE登録名: {get_gss_row_dict[self.const_gss_info["LINE_NAME"]]} スプシ書込完了')

                # 実施を成功欄に日付を書込をする
                self.gss_write.write_data_by_url(gss_info, complete_cell, input_data=str(self.timestamp_two))

            else:
                self.logger.info(f'追加項目なし: {df_filtered}')

            self.logger.info(f'{gss_row_data[self.const_gss_info["NAME"]]}: 処理完了')

        except TimeoutError:
            timeout_comment = "タイムエラー：ログインに失敗している可能性があります。"
            self.logger.error(f'{self.__class__.__name__} {timeout_comment}')
            # エラータイムスタンプ
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp_two)

            # エラーコメント
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=timeout_comment)

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラーが発生 {e}')
            # エラータイムスタンプ
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp_two)

            # エラーコメント
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=timeout_comment)

        finally:
            self._delete_file(csv_path)  # CSVファイルを消去

            # ✅ Chrome を終了
            self.chrome.quit()

    # ----------------------------------------------------------------------------------


    def _read_csv_with_encoding(self, file_path: str) -> pd.DataFrame:
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
            detected_encoding = result["encoding"]
            self.logger.debug(f'判定されたエンコーディング: {detected_encoding}')

        df = pd.read_csv(file_path, encoding=detected_encoding)
        self.logger.debug(f'df: {df.head()}')
        return df

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
