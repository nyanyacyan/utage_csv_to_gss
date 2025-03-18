# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/multi_site_post_flow/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from typing import Dict
from datetime import datetime
from selenium.webdriver.chrome.webdriver import WebDriver

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
from method.base.utils.popup import Popup

# const
from method.const_element import GssInfo, LoginInfo, ErrCommentInfo, PopUpComment

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ

class PrepareFlow:
    def __init__(self, chrome: WebDriver):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

        # 必要info
        self.gss_info = GssInfo.LGRAM.value

        # インスタンス
        self.login = SingleSiteIDLogin(chrome=self.chrome)
        self.random_sleep = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.time_manager = TimeManager()
        self.selenium = SeleniumBasicOperations(chrome=self.chrome)
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

        # const 明確化
        self.const_col_name = self.const_gss_info["NAME"]
        self.const_col_id = self.const_gss_info["ID"]
        self.const_col_password = self.const_gss_info["PASSWORD"]
        self.const_col_reserve_day = self.const_gss_info["RESERVE_DAY"]
        self.const_col_reserve_time = self.const_gss_info["RESERVE_TIME"]
        self.const_col_reel_url = self.const_gss_info["REEL_URL"]
        self.const_col_thumbnail_url = self.const_gss_info["THUMBNAIL_URL"]
        self.const_col_first_type = self.const_gss_info["FIRST_TYPE"]
        self.const_col_first_text = self.const_gss_info["FIRST_TEXT"]
        self.const_col_first_panel_title = self.const_gss_info["FIRST_PANEL_TITLE"]
        self.const_col_first_panel_text = self.const_gss_info["FIRST_PANEL_TEXT"]
        self.const_col_first_panel_button_text = self.const_gss_info[
            "FIRST_PANEL_BUTTON_TEXT"
        ]
        self.const_col_first_panel_url = self.const_gss_info["FIRST_PANEL_URL"]
        self.const_col_second_panel_title = self.const_gss_info["SECOND_PANEL_TITLE"]
        self.const_col_second_panel_text = self.const_gss_info["SECOND_PANEL_TEXT"]
        self.const_col_second_panel_button_text = self.const_gss_info[
            "SECOND_PANEL_BUTTON_TEXT"
        ]
        self.const_col_second_panel_url = self.const_gss_info["SECOND_PANEL_URL"]
        self.const_col_third_timing = self.const_gss_info["THIRD_TIMING"]
        self.const_col_third_text = self.const_gss_info["THIRD_TEXT"]
        self.const_col_post_complete_date = self.const_gss_info["POST_COMPLETE_DATE"]
        self.const_col_error_datetime = self.const_gss_info["ERROR_DATETIME"]
        self.const_col_error_comment = self.const_gss_info["ERROR_COMMENT"]

        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    ####################################################################################
    # 準備工程 スプシチェッカー > 写真のダウンロード > 動画のダウンロード

    def prepare_process(
        self,
        gss_row_data: Dict,
        gss_info: Dict,
        err_datetime_cell: str,
        err_cmt_cell: str,

    ):
        # スプシチェッカー
        check_result, gss_check_err_comment = (
            self.gss_check_err_write._check_gss_values(gss_row_data=gss_row_data)
        )

        # スプシに必要な情報がない場合
        if not check_result:
            self.gss_write._err_write_to_gss(
                gss_info=gss_info,
                err_datetime_cell=err_datetime_cell,
                err_cmt_cell=err_cmt_cell,
                gss_check_err_comment=gss_check_err_comment,
            )
            self.chrome.quit()

        # 写真の取得
        try:
            get_photo_bool, image_path = self.drive_download.get_download_file(
                drive_url=gss_row_data[self.const_gss_info["THUMBNAIL_URL"]],
                sub_dir_name=gss_row_data[self.const_gss_info["NAME"]],
                gss_info=gss_info,
            )

            # 写真ダウンロード中のエラーがあった場合の例外処理
            if not get_photo_bool:
                get_photo_err_comment = self.const_err_comment_dict["GET_PHOTO_ERR"]
                # エラーをスプシに書込
                self.gss_write._err_write_to_gss(
                    gss_info=gss_info,
                    err_datetime_cell=err_datetime_cell,
                    err_cmt_cell=err_cmt_cell,
                    gss_check_err_comment=get_photo_err_comment,
                )
                self.chrome.quit()

            # 動画の取得
            get_movie_bool, movie_path = self.drive_download.get_download_file(
                drive_url=gss_row_data[self.const_gss_info["REEL_URL"]],
                sub_dir_name=gss_row_data[self.const_gss_info["NAME"]],
                gss_info=gss_info,
            )

            # 動画ダウンロード中のエラーがあった場合の例外処理
            if not get_movie_bool:
                get_movie_err_comment = self.const_err_comment_dict["GET_MOVIE_ERR"]
                # エラーをスプシに書込
                self.gss_write._err_write_to_gss(
                    gss_info=gss_info,
                    err_datetime_cell=err_datetime_cell,
                    err_cmt_cell=err_cmt_cell,
                    gss_check_err_comment=get_movie_err_comment,
                )
                self.chrome.quit()


        except Exception as e:
            self.logger.error(f"{self.__class__.__name__}処理中にエラーが発生: {e}")

        self.logger.info(f'【{gss_row_data[self.const_gss_info["NAME"]]}】準備完了')
        self.logger.info(f'image_path: {image_path}\nmovie_path: {movie_path}')
        return image_path, movie_path

# ----------------------------------------------------------------------------------
