# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from typing import Dict
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import os
from io import BytesIO

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.utils.path import BaseToPath
from method.base.utils.fileWrite import FileWrite
from method.base.spreadsheet.spreadsheetWrite import GssWrite

# const
from method.const_str import DriveMime
from method.const_element import ErrCommentInfo


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class GoogleDriveDownload:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.path = BaseToPath()
        self.file_write = FileWrite()
        self.gss_write = GssWrite()

    #!###################################################################################
    # ✅ ダウンロードリクエストを送信

    def get_download_file(self, drive_url: str, sub_dir_name: str, gss_info: Dict):
        self.logger.debug(f'sub_dir_name: {sub_dir_name}')
        drive_service = self._client(gss_info=gss_info)
        file_id = self._extract_file_id(drive_url=drive_url)
        save_path = self._create_download_file_path(gss_info=gss_info, drive_url=drive_url, sub_dir_name=sub_dir_name)

        try:
            #? Google Drive API から fileId に対応するファイルのバイナリデータを取得するリクエストを作成。
            request = drive_service.files().get_media(fileId=file_id)

            #? メモリ上に一時的にバイナリデータを格納できるオブジェクト。
            file_data = BytesIO()

            #? Google Drive API からのデータを少しずつ取得して保存するダウンローダー。
            downloader = MediaIoBaseDownload(file_data, request)

            done = False
            while not done:  # done が True になるまでループ

                # ダウンロードが完了したかどうか（True or False）
                # next_chunk() は、ファイルを分割してダウンロードする関数。
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}% complete.")

            with open(save_path, "wb") as f:
                f.write(file_data.getvalue())

            self.logger.info(f'driveデータファイル書込完了: {save_path}')
            return True, save_path

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} ファイルダウンロード中にエラーが発生: ファイルURL{drive_url}\n{e}')
            return False, None

    #!###################################################################################

    # ----------------------------------------------------------------------------------
    # スプシの認証プロパティ

    def _creds(self, gss_info: Dict):
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        jsonKeyPath = self.path._get_secret_key_path(file_name=gss_info['JSON_KEY_NAME'])
        creds = Credentials.from_service_account_file(jsonKeyPath, scopes=SCOPES)
        return creds

    # ----------------------------------------------------------------------------------
    # Driveへのアクセス

    def _client(self, gss_info: Dict):
        credentials = self._creds(gss_info=gss_info)
        drive_service = build("drive", "v3", credentials=credentials)
        return drive_service

    # ----------------------------------------------------------------------------------
    # GoogleドライブのURLをダウンロード用のURLに変換するためのIDを抽出

    def _extract_file_id(self, drive_url: str):
        if "id=" in drive_url:
            file_id = drive_url.split("id=")[-1]
        elif "drive.google.com/file/d/" in drive_url:
            file_id = drive_url.split("/d/")[1].split("/")[0]
        else:
            self.logger.error(f"❌ Google Drive の URL から file_id を抽出できませんでした: {drive_url}")
            return None  # 例外を発生させず None を返す

        self.logger.debug(f'file_id: {file_id}')
        return file_id

    # ----------------------------------------------------------------------------------
    # 保存先のPathを指定
    #TODO サブディレクトリに拡張子を入れる

    def _get_download_file_path(self, sub_dir_name: str, extension: str, download_file_name: str):
        download_file_path = self.path._get_input_sub_sub_extension_file_path(sub_dir_name=sub_dir_name, extension=extension, file_name=download_file_name)
        self.logger.warning(f"download_file_path: {download_file_path}")
        self.logger.debug(f"download_file_pathの型: {type(download_file_path)}")
        return download_file_path

    # ----------------------------------------------------------------------------------
    # 取得したファイル名と拡張子を入れてフルパス生成

    def _create_download_file_path(self, gss_info: Dict, drive_url: str, sub_dir_name: str):
        # 取得したDriveデータ
        file_name, mime_type = self._get_drive_metadata(gss_info=gss_info, drive_url=drive_url)
        self.logger.debug(f'file_name: {file_name}\nmime_type: {mime_type}')

        mime_type_dict = DriveMime.MIME_TYPE_MAP.value
        file_extension = mime_type_dict.get(mime_type, "")
        only_extension = file_extension.replace(".", "")  # .を取り除く
        self.logger.debug(f'only_extension: {only_extension}')

        if not file_extension:
            self.logger.error(f'{self.__class__.__name__} 想定しているファイル形式ではない: {mime_type}')

        download_file_path = self._get_download_file_path(sub_dir_name=sub_dir_name, extension=only_extension, download_file_name=file_name)

        self.logger.debug(f'download_file_path: {download_file_path}')
        return download_file_path

    # ----------------------------------------------------------------------------------
    # Googleドライブのファイル名とMIMEタイプを取得

    def _get_drive_metadata(self, gss_info: Dict, drive_url: str):
        drive_service = self._client(gss_info=gss_info)
        file_id = self._extract_file_id(drive_url=drive_url)

        # ここでURLを渡している
        file = drive_service.files().get(fileId=file_id, fields="name, mimeType").execute()
        file_name = file["name"]  # ファイル名
        file_mime_type = file["mimeType"]  # 形式

        return file_name, file_mime_type

    # ----------------------------------------------------------------------------------
