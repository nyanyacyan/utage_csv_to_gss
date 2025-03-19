# coding: utf-8

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, shutil
from datetime import datetime
from pathlib import Path


# 自作モジュール
from method.base.utils.logger import Logger
from method.base.utils.path import BaseToPath
from method.base.decorators.decorators import Decorators

decoInstance = Decorators()


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# ファイルに書き込みする基底クラス


class FileMove:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.path = BaseToPath()
        self.currentDate = datetime.now().strftime("%y%m%d_%H%M%S")

    # ----------------------------------------------------------------------------------
    # 結合して書き込む

    def move_csv_dl_to_inputDir(self, sub_dir_name: str, file_name: str, extension: str):
        try:
            downloads_path = self._downloads_path()
            old_path = downloads_path / f"{file_name}{extension}"
            self.logger.debug(f'old_path: {old_path}\n old_path type: {type(old_path)}\nexists: {old_path.exists()}')
            new_path = self._result_dir_path(sub_dir_name=sub_dir_name, file_name=file_name, extension=extension)
            shutil.move(old_path, new_path)
            return new_path

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__}: write_csv_joint: 処理中にエラーが発生{e}')

    # ----------------------------------------------------------------------------------
    # home_path

    def _home_path(self):
        return os.path.expanduser("~")

    # ----------------------------------------------------------------------------------
    # downloads path

    def _downloads_path(self):
        home = self._home_path()
        downloads_path = os.path.join(home, "Downloads")
        self.logger.debug(f'downloads_path: {downloads_path}')
        return downloads_path

    # ----------------------------------------------------------------------------------
    # 移動先のpath

    def _result_dir_path(self, sub_dir_name: str, file_name: str, extension: str):
        return self.path.getResultSubDirFilePath(subDirName=sub_dir_name, fileName=file_name, extension=extension)
