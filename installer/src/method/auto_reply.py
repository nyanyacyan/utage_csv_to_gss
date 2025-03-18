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
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.selenium.get_element import GetElement
from method.base.decorators.decorators import Decorators
from method.base.utils.time_manager import TimeManager
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.base.utils.popup import Popup
from method.base.selenium.click_element import ClickElement

# const
from method.const_element import GssInfo, ErrCommentInfo, PopUpComment, AutoReply

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ

class AutoReplyFlow:
    def __init__(self, chrome: WebDriver):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

        # インスタンス
        self.login = SingleSiteIDLogin(chrome=self.chrome)
        self.random_sleep = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.time_manager = TimeManager()
        self.selenium = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.click_element = ClickElement(chrome=self.chrome)
        self.gss_check_err_write = GssCheckerErrWrite()
        self.popup = Popup()

        # const
        self.const_gss_info = GssInfo.LGRAM.value
        self.const_auto_reply = AutoReply.LGRAM.value
        self.const_err_cmt_dict = ErrCommentInfo.LGRAM.value
        self.popup_cmt = PopUpComment.LGRAM.value

        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    ####################################################################################


    def process(self, gss_row_data: Dict, gss_info: Dict, err_datetime_cell: str, err_cmt_cell: str):
        try:
            # 自動応答をクリック
            self.click_element.clickElement(value=self.const_auto_reply["AUTO_REPLY_BAR_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 自動応答をクリック: 実施済み')
            self.selenium._random_sleep()

            # 新規作成をクリック
            self.click_element.clickElement(value=self.const_auto_reply["NEW_CREATE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 新規作成をクリック: 実施済み')
            self.selenium._random_sleep()

            # 管理名の入力（日付）
            self.click_element.clickClearInput(value=self.const_auto_reply["MANAGEMENT_NAME_INPUT_VALUE"], inputText=self.timestamp)
            self.logger.warning(f'{self.__class__.__name__} 管理名の入力（日付）: 実施済み')
            self.selenium._random_sleep()

            # 自動応答を作成をクリック
            self.click_element.clickElement(value=self.const_auto_reply["AUTO_REPLY_CREATE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 自動応答を作成をクリック: 実施済み')
            self.selenium._random_sleep()

            # 詳細設定に進むをクリック
            self.click_element.clickElement(value=self.const_auto_reply["SETTING_GO_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 詳細設定に進むをクリック: 実施済み')
            self.selenium._random_sleep()

            # 編集するをクリック
            self.click_element.clickElement(value=self.const_auto_reply["EDIT_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 編集するをクリック: 実施済み')
            self.selenium._random_sleep()

            # すべての投稿を選択をクリック
            self.click_element.clickElement(value=self.const_auto_reply["ALL_SELECT_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} すべての投稿を選択をクリック: 実施済み')
            self.selenium._random_sleep()

            # 予約投稿中にあるリストを選択
            reserve_post_list = self.get_element.getElements(by=self.const_auto_reply["RESERVE_POST_LIST_BY"], value=self.const_auto_reply["RESERVE_POST_LIST_VALUE"])
            last_reserve_post = reserve_post_list[0]
            self.logger.info(f'last_reserve_post: {last_reserve_post}')
            self.selenium._random_sleep()

            # 予約投稿中をクリック
            self.chrome.execute_script("arguments[0].click();", last_reserve_post)
            # last_reserve_post.click()
            self.logger.warning(f'{self.__class__.__name__} 予約投稿中をクリック: 実施済み')
            self.selenium._random_sleep()

            # 決定をクリック
            self.click_element.clickElement(value=self.const_auto_reply["DECISION_BTN_VALUE"])
            # self.get_element._enter_tab_chains()  # タブキー→エンターキーを押す
            self.logger.warning(f'{self.__class__.__name__} 決定をクリック: 実施済み')
            self.selenium._random_sleep()

            # 反応時アクションを設定するをクリック
            self.click_element.clickElement(value=self.const_auto_reply["ACTION_SETTING_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 反応時アクションを設定するをクリック: 実施済み')
            self.selenium._random_sleep()

            # アクション登録・編集をクリック
            self.click_element.clickElement(value=self.const_auto_reply["ACTION_EDIT_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} テキストをアクション登録・編集をクリック選択: 実施済み')
            self.selenium._random_sleep()

            # ステップ配信をクリック
            self.click_element.clickElement(value=self.const_auto_reply["STEP_DELIVERY_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} ステップ配信をクリック: 実施済み')
            self.selenium._random_sleep()

            # 開始/再開を選択（ドロップダウン）
            self.get_element._select_element(by=self.const_auto_reply["DELIVERY_SETTING_SELECT_BY"], value=self.const_auto_reply["DELIVERY_SETTING_SELECT_VALUE"], select_value=self.const_auto_reply["DELIVERY_SETTING_SELECT_OPTION_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 開始/再開を選択（ドロップダウン）: 実施済み')
            self.selenium._random_sleep()

            # ステップ配信選択からリストから最後のものを選択
            # reserve_post_list = self.get_element.getElements(by=self.const_auto_reply["RESERVE_POST_LIST_BY"], value=self.const_auto_reply["RESERVE_POST_LIST_VALUE"])
            # last_reserve_post = reserve_post_list[0]
            # self.logger.info(f'last_reserve_post: {last_reserve_post}')

            # ステップ配信選択（ドロップダウン）→ 本日のものを選択する
            self.click_element.clickElement(value=self.const_auto_reply["LAST_RADIO_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} ステップ配信選択（ドロップダウン）: 実施済み')
            self.selenium._random_sleep()

            # アクション設定を保存をクリック
            self.click_element.clickElement(value=self.const_auto_reply["ACTION_SAVE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} アクション設定を保存をクリック: 実施済み')
            self.selenium._random_sleep()

            # 保存をクリック
            self.click_element.clickElement(value=self.const_auto_reply["AUTO_REPLY_SAVE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 保存をクリック: 実施済み')
            self.selenium._random_sleep()

            return True

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラーが発生: {e}')
            return False

# ----------------------------------------------------------------------------------
