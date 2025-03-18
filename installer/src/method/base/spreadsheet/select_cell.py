# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from typing import Dict


# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.errorHandlers import NetworkHandler
from method.base.utils.path import BaseToPath


# ----------------------------------------------------------------------------------
####################################################################################
# **********************************************************************************


class GssSelectCell:
    def __init__(self):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.networkError = NetworkHandler()
        self.path = BaseToPath()


    ####################################################################################
    # ✅ 行のcolumnからセルの列のアルファベットを出力

    def get_cell_address(self, gss_row_dict: Dict, col_name: str, row_num: int):
        col_letter = self._get_col_index(gss_row_dict=gss_row_dict, col_name=col_name)
        cell_address = f"{col_letter}{row_num + 1}"
        self.logger.debug(f'指定のアドレス: {cell_address}')
        return cell_address

    ####################################################################################

    # ----------------------------------------------------------------------------------
    # 1始まりのカラム番号を Excel の A, B, C の形式に変換
    def _col_number_to_letter(self, col_num: int):
        letter = ""
        while col_num > 0:
            col_num, remainder = divmod(col_num -1, 26)
            # chr() は、ASCIIコード（数値）を文字に変換する関数  chr(65)→"A" chr(66)→"B"
            letter = chr(65 + remainder) + letter
        return letter

    # ----------------------------------------------------------------------------------
    # 行のcolumnからセルの列のアルファベットを出力

    def _get_col_index(self, gss_row_dict: Dict, col_name: str):
        col_num = list(gss_row_dict.keys()).index(col_name) + 1
        col_letter = self._col_number_to_letter(col_num=col_num)
        self.logger.debug(f'{col_name} は左から {col_num} 列目 ({col_letter}) にあります。')
        return col_letter

    # ----------------------------------------------------------------------------------
