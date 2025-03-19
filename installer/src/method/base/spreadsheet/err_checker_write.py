# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from typing import Dict

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.utils.popup import Popup

# const
from method.const_element import GssInfo, LoginInfo, ErrCommentInfo

# ----------------------------------------------------------------------------------
####################################################################################
# **********************************************************************************


class GssCheckerErrWrite:
    def __init__(self):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        self.const_gss_info_dict = GssInfo.UTAGE.value
        self.const_login_dict = LoginInfo.UTAGE.value
        self.const_err_cmt_dict = ErrCommentInfo.UTAGE.value
        self.gss_write = GssWrite()
        self.popup = Popup()

        # const
        self.const_gss_info = GssInfo.UTAGE.value
        self.const_login_info = LoginInfo.UTAGE.value
        self.const_err_cmt_dict = ErrCommentInfo.UTAGE.value

        # const 明確化
        self.const_col_name = self.const_gss_info["NAME"]
        self.const_col_id = self.const_gss_info["ID"]
        self.const_col_password = self.const_gss_info["PASSWORD"]
        self.const_col_post_complete_date = self.const_gss_info["POST_COMPLETE_DATE"]
        self.const_col_error_datetime = self.const_gss_info["ERROR_DATETIME"]
        self.const_col_error_comment = self.const_gss_info["ERROR_COMMENT"]

    ####################################################################################
    # ✅ 各columnに入力必須欄の確認してエラーをまとめて返す

    def process(
        self,
        gss_row_data: Dict,
        gss_info: Dict,
        err_datetime_cell: str,
        err_cmt_cell: str,
    ):
        # スプシチェッカー → 必要情報が記載されているかを確認
        check_result, gss_check_err_comment = self._check_gss_values(
            gss_row_data=gss_row_data
        )

        if check_result == False:
            self.logger.error(
                f"エラー内容をスプレッドシートに書込開始\n{gss_check_err_comment}"
            )
            # エラーのタイムスタンプの書込
            self.gss_write.write_data_by_url(
                gss_info=gss_info, cell=err_datetime_cell, input_data=self.time_stamp
            )

            # エラー内容を書込
            self.gss_write.write_data_by_url(
                gss_info=gss_info, cell=err_cmt_cell, input_data=gss_check_err_comment
            )
            self.logger.info("エラー内容書込完了")

            # POPUPを出す
            self.popup.popupCommentOnly(
                popupTitle=self.const_err_cmt_dict["POPUP_TITLE_SHEET_INPUT_ERR"],
                comment=gss_check_err_comment,
            )
            return False
        else:
            return True

    ####################################################################################
    # ----------------------------------------------------------------------------------
    # Gssの必須入力欄確認

    def _check_gss_values(self, gss_row_data: Dict):
        error_comment_list = []
        try:
            if not gss_row_data[self.const_col_id]:  # id確認
                error_comment_list.append(self.const_err_cmt_dict["ERR_GSS_ID"])
            if not gss_row_data[self.const_col_password]:  # pass 確認
                error_comment_list.append(self.const_err_cmt_dict["ERR_GSS_PASS"])
            if not gss_row_data[self.const_col_reserve_day]:  # RESERVE_DAY 確認
                error_comment_list.append( self.const_err_cmt_dict["ERR_GSS_RESERVE_DAY"] )
            if not gss_row_data[self.const_col_reserve_time]:  # RESERVE_TIME 確認
                error_comment_list.append( self.const_err_cmt_dict["ERR_GSS_RESERVE_TIME"] )
            if not gss_row_data[self.const_col_reel_url]:  # REEL_URL 確認
                error_comment_list.append(self.const_err_cmt_dict["ERR_GSS_REEL_URL"])
            if not gss_row_data[self.const_col_thumbnail_url]:  # THUMBNAIL_URL 確認
                error_comment_list.append( self.const_err_cmt_dict["ERR_GSS_THUMBNAIL_URL"] )
            if not gss_row_data[self.const_col_first_type]:  # FIRST_TYPE 確認
                error_comment_list.append(self.const_err_cmt_dict["ERR_GSS_FIRST_TYPE"])
            if not gss_row_data[self.const_col_third_timing]:  # THIRD_TIMING 確認
                error_comment_list.append( self.const_err_cmt_dict["ERR_GSS_THIRD_TIMING"] )
            if not gss_row_data[self.const_col_third_text]:  # THIRD_TEXT 確認
                error_comment_list.append(self.const_err_cmt_dict["ERR_GSS_THIRD_TEXT"])

        # POPUPを出して見えるスプシ変更されてしまったことを促す→スプシのcolumnが変更されてます
        except KeyError as e:
            self.logger.error(
                f"{self.__class__.__name__} スプレッドシートのcolumnの整合性が取れませんでした: {e}"
            )
            raise

        if error_comment_list:
            error_comment = (
                f"スプレッドシートに入力されてない項目があります: {error_comment_list}"
            )
            self.logger.error(f"{self.__class__.__name__} {error_comment}")
            return False, error_comment

        else:
            self.logger.info("必須入力欄、すべて記載確認OK")
            return True, ""

    # ----------------------------------------------------------------------------------
