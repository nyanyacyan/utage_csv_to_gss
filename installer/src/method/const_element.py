#  coding: utf-8
# 文字列をすべてここに保管する
# ----------------------------------------------------------------------------------
# 2024/7/17 更新
# tree -I 'venv|resultOutput|__pycache__'
# ? Command + F10で大文字変換
# ----------------------------------------------------------------------------------
# import
import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


# ----------------------------------------------------------------------------------
# GSS情報


class GssInfo(Enum):

    UTAGE = {
        "JSON_KEY_NAME": "sns-auto-430920-08274ad68b41.json",
        "SHEET_URL": "https://docs.google.com/spreadsheets/d/143M93N4Zr59rNrPCbrsLPDdyt2UakvEN8a1WwHncH7k/edit?gid=1515924776#gid=1515924776",
        "WORKSHEET_NAME": "取得シート",

        # column名
        "CHECK": "チェック",
        "NAME": "Name",
        "ID": "ID",
        "PASSWORD": "Password",

        "ADD_COL": ["LINE友だちID", "LINE登録名", "登録日"],
        "POST_COMPLETE_DATE": "投稿完了日",
        "ERROR_DATETIME": "エラー日時",
        "ERROR_COMMENT": "エラー理由",

        # 選択する
        "TYPE_TEXT": "テキスト",
        "TYPE_PANEL": "パネル",
    }


# ----------------------------------------------------------------------------------
# ログイン情報


class LoginInfo(Enum):

    UTAGE = {
        "LOGIN_URL": "https://go.lgram.jp/",
        "HOME_URL": "https://go.lgram.jp/instagram/account-list",
        "ID_BY": "id",
        "ID_VALUE": "email_login",
        "PASS_BY": "id",
        "PASS_VALUE": "password_login",
        "BTN_BY": "id",
        "BTN_VALUE": "btn_submit_login",
        "LOGIN_AFTER_ELEMENT_BY": "id",
        "LOGIN_AFTER_ELEMENT_VALUE": "show-action-profile",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------


class ErrCommentInfo(Enum):

    UTAGE = {
        # 取得できてない時のコメント
        "ERR_GSS_ID": "[ID]",
        "ERR_GSS_PASS": "[Password]",
        "ERR_GSS_RESERVE_DAY": "[投稿予約日]",
        "ERR_GSS_RESERVE_TIME": "[投稿予約時間]",
        "ERR_GSS_REEL_URL": "[リールURL]",
        "ERR_GSS_THUMBNAIL_URL": "[サムネイルURL]",
        "ERR_GSS_FIRST_TYPE": "[1通目_タイプ]",
        "ERR_GSS_THIRD_TIMING": "[3通目_タイミング]",
        "ERR_GSS_THIRD_TEXT": "[3通目_テキスト_テキスト]",

        # POPUP_TITLE
        "POPUP_TITLE_SHEET_INPUT_ERR": "スプレッドシートをご確認ください。",
        "POPUP_TITLE_FACEBOOK_LOGIN_ERR": "ログインが必要です",
        "POPUP_COMMENT_FACEBOOK_LOGIN_ERR": "Facebookのログインが必要になります。",
        "": "",
        "": "",
        "": "",
        "": "",
        # 正しくダウンロードできなかった時のコメント
        "GET_PHOTO_ERR": "写真のダウンロードに失敗",
        "GET_MOVIE_ERR": "動画のダウンロードに失敗",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------


class PopUpComment(Enum):
    UTAGE = {
        "ALL_COMPLETE_TITLE": "完了通知",
        "ALL_COMPLETE_COMMENT": "すべての処理が完了しました。エラー内容をご確認ください",
        "": "",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------

class Element(Enum):
    UTAGE = {
        "MATCH_RULES_BY": "",
        "MATCH_RULES_VOL": "",
        "MATCH_CHOICE_BY": "",
        "MATCH_CHOICE_VOL": "",
        "MATCH_CHOICE_SELECT_VOL": "",
        "DATE_INPUT_BY": "",
        "DATE_INPUT_VOL": "",
        "sorting_by": "",
        "SORTING_BY": "",
        "SORTING_VOL": "",
        "CSV_OUTPUT_BY": "",
        "CSV_OUTPUT_VOL": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",

    }

# ----------------------------------------------------------------------------------


