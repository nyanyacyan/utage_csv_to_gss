# coding: utf-8

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

import glob, os, chardet
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from fpdf import FPDF
import aiofiles


# 自作モジュール
from method.base.utils.logger import Logger
from method.const_str import Extension, SubDir
from method.base.utils.path import BaseToPath
from method.base.selenium.errorHandlers import FileWriteError
from method.base.decorators.decorators import Decorators

decoInstance = Decorators()


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# ファイルに書き込みする基底クラス


class FileJoint:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.path = BaseToPath()
        self.currentDate = datetime.now().strftime("%y%m%d_%H%M%S")

    # ----------------------------------------------------------------------------------
    # 結合して書き込む

    def write_csv_joint(self, csv_folder_path: str, output_path: str, sheet_name: str):
        try:
            merged_df = self._join_csv(csv_folder_path=csv_folder_path)
            self._write_excel(output_path=output_path, merged_df=merged_df, sheet_name=sheet_name)
            self.logger.info(f'書込完了')

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__}: write_csv_joint: 処理中にエラーが発生{e}')

    # ----------------------------------------------------------------------------------
    # 特定のフォルダのCSVファイルを結合

    def _write_excel(self, output_path: str, merged_df: pd.DataFrame, sheet_name: str):
        with pd.ExcelWriter(output_path) as writer:
            merged_df.to_excel(writer, sheet_name=sheet_name)

    # ----------------------------------------------------------------------------------
    # ファイル結合

    def _join_csv(self, csv_folder_path: str):
        csv_files = glob.glob(os.path.join(csv_folder_path, "*.csv"))
        df_list = []
        for file in csv_files:
            encoding = self.detect_encoding(file)
            self.logger.debug(f'encoding: {encoding}')
            df = pd.read_csv(file, encoding=encoding)

            df_list.append(df)  # この時点では各ファイルのcolumnが混在
        merged_df = pd.concat(df_list, ignore_index=True)  # concatでcolumnなどの無駄な部分を削除
        self.logger.debug(f'merged_df: {merged_df.head()}')
        return merged_df

    # ----------------------------------------------------------------------------------
    # encodingを判定

    def detect_encoding(self, file_path: str):
        with open(file_path, "rb") as file:
            raw_data = file.read(10000)
            result = chardet.detect(raw_data)
            return result["encoding"]

    # ----------------------------------------------------------------------------------


if __name__ == "__main__":
    currentDate = datetime.now().strftime("%m%d")

    csv_folder_path = "/Users/nyanyacyan/Downloads/Instagram"
    output_path = f"/Users/nyanyacyan/Downloads/Instagram_コメント集計{currentDate}.xlsx"
    sheet_name = "Instagram_元データ"

    # csv_folder_path = "/Users/nyanyacyan/Downloads/Facebook"
    # output_path = f"/Users/nyanyacyan/Downloads/Facebook_コメント集計{currentDate}.xlsx"
    # sheet_name = "Facebook_元データ"

    file_joint = FileJoint()
    file_joint.write_csv_joint(csv_folder_path=csv_folder_path, output_path=output_path, sheet_name=sheet_name)
