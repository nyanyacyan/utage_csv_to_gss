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

    LGRAM = {
        "JSON_KEY_NAME": "sns-auto-430920-08274ad68b41.json",
        "SHEET_URL": "https://docs.google.com/spreadsheets/d/1cpJkt9llIEYGMzEeYsM15By2BfIVG7GS-m-3oaXw7hI/edit?gid=0#gid=0",
        "WORKSHEET_NAME": "シート1",

        # column名
        "CHECK": "チェック",
        "NAME": "Name",
        "ID": "ID",
        "CAPTION": "キャプション",
        "PASSWORD": "Password",
        "RESERVE_DAY": "投稿予約日",
        "RESERVE_TIME": "投稿予約時間",
        "REEL_URL": "リールURL",
        "THUMBNAIL_URL": "サムネイルURL",
        "FIRST_TYPE": "1通目_タイプ",
        "FIRST_TEXT": "1通目_テキスト_テキスト",
        "FIRST_PANEL_TITLE": "1通目_パネル_タイトル",
        "FIRST_PANEL_TEXT": "1通目_パネル_テキスト",
        "FIRST_PANEL_BUTTON_TEXT": "1通目_パネル_ボタンテキスト",
        "FIRST_PANEL_URL": "1通目_パネル_URL",
        "SECOND_CHECK": "2通目_チェック",
        "SECOND_PANEL_TITLE": "2通目_パネル_タイトル",
        "SECOND_PANEL_TEXT": "2通目_パネル_テキスト",
        "SECOND_PANEL_BUTTON_TEXT": "2通目_パネル_ボタンテキスト",
        "SECOND_PANEL_URL": "2通目_パネル_URL",
        "THIRD_TIMING": "3通目_タイミング",
        "THIRD_TEXT": "3通目_テキスト_テキスト",
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

    LGRAM = {
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

    LGRAM = {
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
    LGRAM = {
        "ALL_COMPLETE_TITLE": "完了通知",
        "ALL_COMPLETE_COMMENT": "すべての処理が完了しました。エラー内容をご確認ください",
        "": "",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------

class Post(Enum):
    LGRAM = {
        "SELECT_ACCOUNT_BY": "css",
        "SELECT_ACCOUNT_VALUE": ".name-bot",
        "FACEBOOK_CLOSE_BY": "css",
        "FACEBOOK_CLOSE_VALUE": ".close-v3.position-absolute",
        "IF_FACEBOOK_BY": "css",
        "IF_FACEBOOK_VALUE": "//button[contains(@class, 'btn') and contains(@class, 'btn-edf4fB-color') and .//span[normalize-space()='Facebookログインへ進む']]",
        "POST_EXTENSIONS_VALUE": "//span[contains(text(), '投稿機能')]",
        "POST_CREATE_VALUE": "//span[contains(text(), '投稿作成')]",
        "PLUS_POST_CREATE_VALUE": "//button//span[contains(text(), '投稿作成')]",
        "MANAGEMENT_NAME_BY": "css",
        "MANAGEMENT_NAME_VALUE": "div.modal-body input[name='scenario_name']",
        "MANAGEMENT_NAME_INPUT_TEXT": "自動投稿",
        "MANAGEMENT_NAME_BTN_BY": "css",
        "MANAGEMENT_NAME_BTN_VALUE": "div.modal-footer span[data-dismiss='modal']",
        "REEL_SELECT_BTN_VALUE": "//div[@class='post-type-box-title'][p[text()='リールの投稿']]",
        "REEL_SELECT_POST_BTN_VALUE": "//button[contains(span/text(), '投稿編集へ進む')]",
        "IMAGE_SELECT_BTN_VALUE": "//button[contains(@class, 'btn-5799db-color') and contains(@class, 'btn-sm') and span[text()='画像を変更する']]",
        "GO_SETTING_BTN_VALUE": "//button[span[text()='詳細設定へ進む']]",
        "RETURN_GO_SETTING_BTN_VALUE": "//button[span[text()='詳細設定へ進む']]",
        "DATE_INPUT_VALUE": "//input[@type='date' and @name='date_send']",
        "TIME_INPUT_VALUE": "//input[@type='text' and @name='time_send']",
        "CAPTION_INPUT_VALUE": "//textarea[@id='post_caption']",
        "GO_CHECK_BTN_VALUE": "//button[span[text()='設定内容を確認して投稿に進む']]",
        "GO_POST_BTN_VALUE": "//button[span[text()='この内容で投稿する']]",
        "": "",
        "": "",

    }

# ----------------------------------------------------------------------------------

class TagManagement(Enum):
    LGRAM = {
        "TAG_MANAGEMENT_BAR_VALUE": "//div[contains(@class, 'i-sidebar-item-wp')]//span[contains(text(), 'タグ管理')]",
        "UN_CATEGORIZE_BTN_VALUE": "//li[contains(@class, 'folder-active')]//span[contains(text(), '未分類')]",
        "EXITS_PROGRESS_TAG_VALUE": "//td[@class='pl-2']//span[contains(text(), '対応中')]",
        "CREATE_TAG_VALUE": "//button[contains(@class, 'btn-5799db-color') and span/span[contains(text(), 'タグ新規作成')]]",
        "SELECT_TAG_MANAGEMENT_VALUE": "//td[@class='pl-2']//span[contains(text(), '対応中')]",
        "PROGRESS_TAG_VALUE": "対応中",
        "TAG_MANAGEMENT_NAME_VALUE": "//input[@name='item_name' and @placeholder='管理名を入力してください']",
        "CREATE_BTN_VALUE": "//button[contains(@class, 'btn-f4f0fd-color') and span[text()='作成する']]",
        "SAVE_BTN_VALUE": "//button[contains(@class, 'btn-save-item') and normalize-space()='保存する']",
        "": "",
        "": "",
    }

# ----------------------------------------------------------------------------------
class StepDelivery(Enum):
    LGRAM = {
        "SELECT_STEP_DELIVERY_VALUE": "//a[contains(@href, 'instagram/scenario')]//span[text()='ステップ配信']",
        "NEW_CREATE_BTN_VALUE": "//button[contains(@class, 'btn-5799db-color')]//span[contains(text(), '新規作成')]",
        "MANAGEMENT_NAME_INPUT_TEXT": "ステップ配信",
        "MANAGEMENT_NAME_VALUE": "//input[contains(@class, 'form-control') and @name='scenario_name']",
        "GO_MESSAGE_BTN_VALUE": "//div[contains(@class, 'modal-footer')]//button[span[text()='メッセージの登録に進む']]",
        "DELIVERY_TIMING_BTN_VALUE": "//button[contains(@style, 'min-width: 110px') and div/span[text()='配信タイミング']]",
        "STEP_NAME_INPUT_TEXT": "タイミング",
        "STEP_NAME_INPUT_VALUE": "//input[@data-vv-scope='deliveryTimingSelectModal' and @name='step_name']",
        "DO_IT_NOW_BTN_VALUE": "//label[div/div/span[text()='ステップ開始直後']]/div/input[@type='radio']",
        "GO_BTN_VALUE": "//div[contains(@class, 'modal-footer')]//button[span[text()='進む']]",
        "CREATE_MESSAGE_VALUE": "//button[contains(@class, 'btn-outline-5799db-color') and contains(@class, 'none-disable-style')][div/span[text()='メッセージ作成']]",
        "SELECT_TEXT_BTN_VALUE": "//div[contains(@class, 'card')]//p[contains(@class, 'font-s16')]//span[contains(text(), 'テキスト')]",
        "GO_SETTING_BTN_VALUE": "//div[contains(@class, 'text-center')]//button[contains(@class, 'btn-select-template-type') and span[contains(text(), '詳細設定へ進む')]]",
        "FIRST_TEXT_AREA_VALUE": "//div[contains(@class, 'col-md-12')]//textarea[@id='text_message']",
        "SAVE_BTN_VALUE": "//div[contains(@class, 'mt-5') and contains(@class, 'mb-5')]//button[contains(@class, 'instagram-btn-save') and contains(text(), '保存')]",
        "": "",
        "": "",
        "SELECT_PANEL_BTN_VALUE": "//div[contains(@class, 'card')]//p[contains(@class, 'font-s16')]//span[contains(text(), 'パネルボタン')]",
        "PANEL_TITLE_TEXTAREA_VALUE": "//div[contains(@class, 'form-group') and contains(@class, 'mb-0')]//textarea[@name='panel_text_0']",
        "PANEL_TEXT_TEXTAREA_VALUE": "//textarea[contains(@class, 'form-control') and contains(@class, 'form-control-e0e0e0-border')]",
        "PANEL_BTN_TEXT_VALUE": "//div[contains(@class, 'ml-18px')]//input[@name='button_text_0_0']",
        "PANEL_URL_VALUE": "//input[@name='url_0_0']",
        "PANEL_SAVE_BTN_VALUE": "//div[contains(@class, 'mt-5') and contains(@class, 'mb-5')]//button[contains(@class, 'instagram-btn-save')]",
        "": "",
        "": "",

        # third
        "HIDDEN_ELEMENT_BTN_VALUE": "//div[contains(@class, 'toggle-filter-btn') and contains(@class, 'tutorial-wp')]",
        "DELIVERY_SUBJECT_VALUE": "//div[contains(@class, 'add-filter-btn')]//span[contains(text(), '配信対象追加')]",
        "FILTERING_BTN_VALUE": "//button[contains(@class, 'btn-outline-5799db-color')]//span[contains(text(), '絞り込み条件 編集')]",
        "TAG_BTN_VALUE": "//div[contains(@class, 'button-item')]//span[text()='タグ']",
        "OPTION_VALUE": "2",
        "SELECT_DROPDOWN_VALUE": "//select[contains(@class, 'form-control') and contains(@class, 'my_class')]",
        "PROGRESS_TAG_BTN_VALUE": "//ul[@class='folder-item-selection']//li[label[contains(.,'対応中')]]//input[@type='checkbox']",
        "FILTERING_SAVE_BTN_VALUE": "//div/button[@type='button' and contains(@class, 'btn-7b56e0-color')][span[text()='保存']]",
        "FILTERING_CHECK_WORD_VALUE": "//div[@class='preview-filter-text-right-bottom']/span/span[contains(text(), '選択したタグが1つでも付いている人')]",
        "FILTERING_STEP_NAME_INPUT_TEXT": "フィルタリング",
        "ELAPSED_TIME_BTN_VALUE": "//input[@type='radio' and @value='2']/following-sibling::div[contains(@class, 'step-time-top')]//span[text()='経過時間で指定']",
        "INPUT_MINUTES_VALUE": "//span[text()='時間']/following-sibling::input[@type='number']",
        "RESERVE_GO_BTN_BY": "css",
        "RESERVE_GO_BTN_VALUE": ".modal-footer .btn-outline-7b56e0-color",
        "": "",
        "": "",
        "": "",
        "": "",

    }

# ----------------------------------------------------------------------------------

class AutoReply(Enum):
    LGRAM = {
        "AUTO_REPLY_BAR_VALUE": "//div[contains(@class, 'i-sidebar-item-wp')]//span[contains(text(), '自動応答')]",
        "NEW_CREATE_BTN_VALUE": "//button[contains(@class, 'btn-5799db-color')]//span[contains(text(), '新規作成')]",
        "MANAGEMENT_NAME_INPUT_VALUE": "//input[@data-vv-scope='trigger_modal' and @data-vv-as='管理名']",
        "AUTO_REPLY_CREATE_BTN_VALUE": "//button[contains(@class, 'btn-outline-7b56e0-color') and contains(@class, 'btn-lg') and .//span[normalize-space()='自動応答を作成']]",
        "SETTING_GO_BTN_VALUE": "//div[contains(@class, 'modal-footer')]//button[contains(@class, 'btn') and contains(@class, 'color-7B56E0')]//span[normalize-space()='詳細設定へ進む']",
        "EDIT_BTN_VALUE": "//button[contains(@class, 'btn-f4f0fd-color') and contains(@style, 'min-width: 130px')]//span[normalize-space()='編集する']",
        "ALL_SELECT_BTN_VALUE": "//button[contains(@class, 'check-all')]//span[normalize-space()='全ての投稿を選択する（今後の投稿も自動的に対象となります）']",
        "RESERVE_POST_LIST_BY": "css",
        "RESERVE_POST_LIST_VALUE": "label.post-card-wp",
        "DECISION_BTN_VALUE": "//div[@class='modal-footer']//button[contains(@class, 'btn-f4f0fd-color')]//span[normalize-space()='決定']",
        "ACTION_SETTING_VALUE": "//div[@class='col-12']/a[span[normalize-space(text())='反応時アクションを設定する >']]",
        "ACTION_EDIT_BTN_VALUE": "//div[@class='rounded-3']//button[contains(@class, 'btn-5799db-color') and span[text()='アクション登録・編集']]",
        "STEP_DELIVERY_BTN_VALUE": "//div[@class='add-action-buttons modal-action-scrollbar light-scrollbar-track']//div[@class='button-item' and span[text()='ステップ配信']]",
        "DELIVERY_SETTING_SELECT_BY": "css",
        "DELIVERY_SETTING_SELECT_VALUE": "select.form-control.font-s14.font-w3.color-888888.text-center.w-100.py-2.no-arrows",
        "DELIVERY_SETTING_SELECT_OPTION_VALUE": "2",
        "LAST_RADIO_BTN_VALUE": "(//ul[@class='folder-item-selection']/li/label/input[@type='radio'])[last()]",
        "ACTION_SAVE_BTN_VALUE": "//div[@class='modal-footer']//button[contains(@class, 'btn-d4c7f8-color') and contains(text(), '保 存')]",
        "AUTO_REPLY_SAVE_BTN_VALUE": "//button[contains(@class, 'btn-f4f0fd-color') and contains(span, '保存')]",

    }
