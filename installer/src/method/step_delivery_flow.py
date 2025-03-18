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
from method.base.selenium.click_element import ClickElement
from method.base.decorators.decorators import Decorators
from method.base.utils.time_manager import TimeManager
from method.base.spreadsheet.select_cell import GssSelectCell
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.base.utils.popup import Popup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# const
from method.const_element import GssInfo, ErrCommentInfo, StepDelivery, Post

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ

class StepDeliveryFlow:
    def __init__(self, chrome: WebDriver):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

        # インスタンス
        self.login = SingleSiteIDLogin(chrome=self.chrome)
        self.selenium = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.time_manager = TimeManager()
        self.get_element = GetElement(chrome=self.chrome)
        self.click_element = ClickElement(chrome=self.chrome)
        self.select_cell = GssSelectCell()
        self.gss_check_err_write = GssCheckerErrWrite()
        self.popup = Popup()

        # const
        self.const_gss_info = GssInfo.LGRAM.value
        self.const_err_cmt_dict = ErrCommentInfo.LGRAM.value

        self.const_post = Post.LGRAM.value
        self.const_step_delivery = StepDelivery.LGRAM.value

        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    ####################################################################################
    # ----------------------------------------------------------------------------------
    # 1通目
    # ステップ配信flow

    def first_process(self, gss_row_data: Dict, gss_info: Dict, err_datetime_cell: str, err_cmt_cell: str):
        try:
            # ステップ配信をクリック
            self.click_element.clickElement(value=self.const_step_delivery["SELECT_STEP_DELIVERY_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} ステップ配信をクリック: 実施済み')
            self.selenium._random_sleep()

            # 新規作成をクリック
            self.click_element.clickElement(value=self.const_step_delivery["NEW_CREATE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 新規作成をクリック: 実施済み')
            self.selenium._random_sleep()

            # 管理名の入力（日付）
            self.click_element.clickClearInput(value=self.const_step_delivery["MANAGEMENT_NAME_VALUE"], inputText=self.timestamp)
            # self.get_element._enter_tab_chains()  # タブキー→エンターキーを押す
            self.logger.warning(f'{self.__class__.__name__} 管理名の入力（日付）: 実施済み')
            self.selenium._random_sleep()

            # メッセージを登録に進む
            self.click_element.clickElement(value=self.const_step_delivery["GO_MESSAGE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} メッセージを登録に進む: 実施済み')
            self.selenium._random_sleep()

            # 配信タイミング
            self.click_element.clickElement(value=self.const_step_delivery["DELIVERY_TIMING_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 配信タイミング: 実施済み')
            self.selenium._random_sleep()

            # ステップ名を入力
            self.click_element.clickClearInput(value=self.const_step_delivery["STEP_NAME_INPUT_VALUE"], inputText=self.timestamp)
            self.logger.warning(f'{self.__class__.__name__} ステップ名を入力: 実施済み: {self.timestamp}')
            self.selenium._random_sleep()

            # 進むをクリック(初期位置をそのまま活かす)
            self.click_element.clickElement(value=self.const_step_delivery["GO_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 進むをクリック: 実施済み')
            self.selenium._random_sleep()

            # メッセージを作成をクリック
            self.click_element.clickElement(value=self.const_step_delivery["CREATE_MESSAGE_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} メッセージを作成をクリック: 実施済み')
            self.selenium._random_sleep()

            # 選択する テキスト or PDF
            self._first_choice_text_or_pdf(gss_row_data=gss_row_data)

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラー発生中: {e}')
            error_comment = f"【1通目】処理中にエラーが発生: {e}"

            # エラータイムスタンプ
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp)

            # エラーコメント
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=error_comment)
            self.chrome.quit()
            raise

    # ----------------------------------------------------------------------------------
    # ステップ配信flow

    def second_process(self, gss_row_data: Dict, gss_info: Dict, err_datetime_cell: str, err_cmt_cell: str):
        if not gss_row_data[gss_info["SECOND_CHECK"]] == "TRUE":
            self.logger.warning(f'{self.__class__.__name__} 2通目の利用なしのためスキップ: {gss_row_data[gss_info["NAME"]]}')
            return
        else:
            self.logger.info(f'2通目手順開始: {gss_row_data[gss_info["NAME"]]}')

        try:
            # メッセージを作成をクリック
            self.click_element.clickElement(value=self.const_step_delivery["CREATE_MESSAGE_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} メッセージを作成をクリック: 実施済み')
            self.selenium._random_sleep()

            # パネルプロセス
            self._second_panel_type_process(gss_row_data=gss_row_data)

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラー発生中: {e}')
            error_comment = f"【2通目】処理中にエラーが発生: {e}"

            # エラータイムスタンプ
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp)

            # エラーコメント
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=error_comment)
            raise

    # ----------------------------------------------------------------------------------
    # ステップ配信flow

    def third_process(self, gss_row_data: Dict, gss_info: Dict, err_datetime_cell: str, err_cmt_cell: str):
        try:
            # ステップ購読者全員の矢印をクリック
            self.click_element.clickElement(value=self.const_step_delivery["HIDDEN_ELEMENT_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} ステップ購読者全員の矢印をクリック: 実施済み')
            self.selenium._random_sleep()

            # 配信対象追加をクリック
            self.click_element.clickElement(value=self.const_step_delivery["DELIVERY_SUBJECT_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 配信対象追加をクリック: 実施済み')
            self.selenium._random_sleep()

            # 絞り込み条件追加をクリック
            self.click_element.clickElement(value=self.const_step_delivery["FILTERING_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 絞り込み条件追加をクリック: 実施済み')
            self.selenium._random_sleep()

            # タグをクリック
            self.click_element.clickElement(value=self.const_step_delivery["TAG_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} タグをクリック: 実施済み')
            self.selenium._random_sleep()

            # ドロップダウンメニューをクリック
            self.get_element._select_element(value=self.const_step_delivery["SELECT_DROPDOWN_VALUE"], select_value=self.const_step_delivery["OPTION_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} ドロップダウンメニューをクリック: 実施済み')
            self.selenium._random_sleep()

            # 対応中をクリック
            self.click_element.clickElement(value=self.const_step_delivery["PROGRESS_TAG_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 対応中をクリック: 実施済み')
            self.selenium._random_sleep()

            # 保存をクリック（ここでかなりの時間がかかる→何かしらで判断が必要→対応中 選択したタグが一つでも。。この部分があるかどうかで判断してもいいかも）
            self.click_element.clickElement(value=self.const_step_delivery["FILTERING_SAVE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 保存をクリック: 実施済み')
            self.selenium._random_sleep()

            #! 対応中 選択したタグが出てくるまで待機（最大60秒）
            try:
                WebDriverWait(self.chrome, 60).until( EC.presence_of_element_located((By.XPATH, self.const_step_delivery["FILTERING_CHECK_WORD_VALUE"])) )
                self.logger.info(f'条件設定、完了しました。')

            except TimeoutException:
                self.logger.error(f'{self.__class__.__name__} 条件設定に失敗しています')

                # TODO ここのエラー内容をスプシに書き込む


            # 配信タイミングをクリック
            self.click_element.clickElement(value=self.const_step_delivery["DELIVERY_TIMING_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 配信タイミングをクリック: 実施済み')
            self.selenium._random_sleep()

            # ステップ名の入力
            self.click_element.clickClearInput(value=self.const_step_delivery["STEP_NAME_INPUT_VALUE"], inputText=self.timestamp)
            self.logger.warning(f'{self.__class__.__name__} ステップ名を入力: 実施済み: {self.timestamp}')
            self.selenium._random_sleep()

            # 経過時間で指定をクリック（選択）
            self.click_element.clickElement(value=self.const_step_delivery["ELAPSED_TIME_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 経過時間で指定をクリック: 実施済み')
            self.selenium._random_sleep()

            # 進むをクリック
            self.click_element.clickElement(value=self.const_step_delivery["GO_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 進むをクリック: 実施済み')
            self.selenium._random_sleep()

            # 分を入力（1〜7から選択）
            minute_data = gss_row_data[self.const_gss_info["THIRD_TIMING"]]
            self.logger.debug(f'minute_data: {minute_data}')
            self.click_element.clickClearInput(value=self.const_step_delivery["INPUT_MINUTES_VALUE"], inputText=minute_data)
            self.logger.warning(f'{self.__class__.__name__} 分を入力: 実施済み')
            self.selenium._random_sleep()

            # 進むをクリック
            self.click_element.clickElement(value=self.const_step_delivery["INPUT_MINUTES_VALUE"])
            # self.click_element.clickElement(by=self.const_step_delivery["RESERVE_GO_BTN_BY"], value=self.const_step_delivery["RESERVE_GO_BTN_VALUE"])
            self.get_element._enter_tab_chains()
            self.logger.warning(f'{self.__class__.__name__} 進むをクリック: 実施済み')
            self.selenium._random_sleep()

            # メッセージ作成をクリック
            self.click_element.clickElement(value=self.const_step_delivery["CREATE_MESSAGE_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} メッセージを作成をクリック: 実施済み')
            self.selenium._random_sleep()

            # テキストプロセス
            self._third_text_type_process(gss_row_data=gss_row_data)

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラー発生中: {e}')
            error_comment = f"【3通目】処理中にエラーが発生: {e}"

            # エラータイムスタンプ
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp)

            # エラーコメント
            self.gss_write.write_data_by_url(gss_info=gss_info, cell=err_cmt_cell, input_data=error_comment)
            raise

    # ----------------------------------------------------------------------------------
    # 1通目
    # テキスト or PDF

    def _first_choice_text_or_pdf(self, gss_row_data: Dict):
        try:
            gss_first_type = gss_row_data[self.const_gss_info["FIRST_TYPE"]]

            # テキストを選択
            if gss_first_type == self.const_gss_info["TYPE_TEXT"]:
                self.logger.info(f'テキストタイプを選択')
                self._first_text_type_process(gss_row_data=gss_row_data)  # テキストプロセス

            # パネルボタンを選択
            elif gss_first_type == self.const_gss_info["TYPE_PANEL"]:
                self.logger.info(f'パネルボタンタイプを選択')
                self._first_panel_type_process(gss_row_data=gss_row_data)  # パネルプロセス

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラー発生中: {e}')

    # ----------------------------------------------------------------------------------
    # 1通目
    # テキストタイプの定義

    def _first_text_type_process(self, gss_row_data: Dict):
        try:
            # テキストを選択
            self.click_element.clickElement(value=self.const_step_delivery["SELECT_TEXT_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} テキストを選択: 実施済み')
            self.selenium._random_sleep()

            # 詳細設定に進むをクリック
            self.click_element.clickElement(value=self.const_step_delivery["GO_SETTING_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 詳細設定に進むをクリック: 実施済み')
            self.selenium._random_sleep()

            # テキストを入力
            first_text = gss_row_data[self.const_gss_info["FIRST_TEXT"]]
            self.click_element.clickClearInput(value=self.const_step_delivery["FIRST_TEXT_AREA_VALUE"], inputText=first_text)
            self.logger.warning(f'{self.__class__.__name__} テキストを入力: 実施済み')
            self.selenium._random_sleep()

            # 保存をクリック
            self.click_element.clickElement(value=self.const_step_delivery["SAVE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 保存をクリック: 実施済み')
            self.selenium._random_sleep()

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラー発生中: {e}')

    # ----------------------------------------------------------------------------------
    # 1通目
    # パネルタイプの定義

    def _first_panel_type_process(self, gss_row_data: Dict):
        try:
            # パネルボタンを選択
            self.click_element.clickElement(value=self.const_step_delivery["SELECT_PANEL_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} パネルボタンを選択: 実施済み')
            self.selenium._random_sleep()

            # 詳細設定に進むをクリック
            self.click_element.clickElement(value=self.const_step_delivery["GO_SETTING_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 詳細設定に進むをクリック: 実施済み')
            self.selenium._random_sleep()

            # タイトルを入力
            first_title = gss_row_data[self.const_gss_info["FIRST_PANEL_TITLE"]]
            self.click_element.clickClearInput(value=self.const_step_delivery["PANEL_TITLE_TEXTAREA_VALUE"], inputText=first_title)
            self.logger.warning(f'{self.__class__.__name__} タイトルを入力: 実施済み')
            self.selenium._random_sleep()

            # テキスト入力
            first_text = gss_row_data[self.const_gss_info["FIRST_PANEL_TEXT"]]
            self.click_element.clickClearInput(value=self.const_step_delivery["PANEL_TEXT_TEXTAREA_VALUE"], inputText=first_text)
            self.logger.warning(f'{self.__class__.__name__} テキストを入力: 実施済み')
            self.selenium._random_sleep()

            # ボタンテキストを入力
            first_btn_text = gss_row_data[self.const_gss_info["FIRST_PANEL_BUTTON_TEXT"]]
            self.click_element.clickClearInput(value=self.const_step_delivery["PANEL_BTN_TEXT_VALUE"], inputText=first_btn_text)
            self.logger.warning(f'{self.__class__.__name__} ボタンテキストを入力: 実施済み')
            self.selenium._random_sleep()

            # URLを入力
            first_url = gss_row_data[self.const_gss_info["FIRST_PANEL_URL"]]
            self.click_element.clickClearInput(value=self.const_step_delivery["PANEL_URL_VALUE"], inputText=first_url)
            self.logger.warning(f'{self.__class__.__name__} URLを入力: 実施済み')
            self.selenium._random_sleep()

            # 保存をクリック
            self.click_element.clickElement(value=self.const_step_delivery["PANEL_SAVE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 保存をクリック: 実施済み')
            self.selenium._random_sleep()

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラー発生中: {e}')

    # ----------------------------------------------------------------------------------
    # 2通目
    # パネルタイプの定義

    def _second_panel_type_process(self, gss_row_data: Dict):
        try:
            # パネルボタンを選択
            self.click_element.clickElement(value=self.const_step_delivery["SELECT_PANEL_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} パネルボタンを選択: 実施済み')
            self.selenium._random_sleep()

            # 詳細設定に進むをクリック
            self.click_element.clickElement(value=self.const_step_delivery["GO_SETTING_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 詳細設定に進むをクリック: 実施済み')
            self.selenium._random_sleep()

            # タイトルを入力
            first_title = gss_row_data[self.const_gss_info["SECOND_PANEL_TITLE"]]
            self.click_element.clickClearInput(value=self.const_step_delivery["PANEL_TITLE_TEXTAREA_VALUE"], inputText=first_title)
            self.logger.warning(f'{self.__class__.__name__} タイトルを入力: 実施済み')
            self.selenium._random_sleep()

            # テキスト入力
            first_text = gss_row_data[self.const_gss_info["SECOND_PANEL_TEXT"]]
            self.click_element.clickClearInput(value=self.const_step_delivery["PANEL_TEXT_TEXTAREA_VALUE"], inputText=first_text)
            self.logger.warning(f'{self.__class__.__name__} テキストを入力: 実施済み')
            self.selenium._random_sleep()

            # ボタンテキストを入力
            first_btn_text = gss_row_data[self.const_gss_info["SECOND_PANEL_BUTTON_TEXT"]]
            self.click_element.clickClearInput(value=self.const_step_delivery["PANEL_BTN_TEXT_VALUE"], inputText=first_btn_text)
            self.logger.warning(f'{self.__class__.__name__} ボタンテキストを入力: 実施済み')
            self.selenium._random_sleep()

            # URLを入力
            first_url = gss_row_data[self.const_gss_info["SECOND_PANEL_URL"]]
            self.click_element.clickClearInput(value=self.const_step_delivery["PANEL_URL_VALUE"], inputText=first_url)
            self.logger.warning(f'{self.__class__.__name__} URLを入力: 実施済み')
            self.selenium._random_sleep()

            # 保存をクリック
            self.click_element.clickElement(value=self.const_step_delivery["PANEL_SAVE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 保存をクリック: 実施済み')
            self.selenium._random_sleep()

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラー発生中: {e}')

    # ----------------------------------------------------------------------------------
    # 3通目
    # テキストタイプの定義

    def _third_text_type_process(self, gss_row_data: Dict):
        try:
            # テキストを選択
            self.click_element.clickElement(value=self.const_step_delivery["SELECT_TEXT_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} テキストを選択: 実施済み')
            self.selenium._random_sleep()

            # 詳細設定に進むをクリック
            self.click_element.clickElement(value=self.const_step_delivery["GO_SETTING_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 詳細設定に進むをクリック: 実施済み')
            self.selenium._random_sleep()

            # テキストを入力
            second_text = gss_row_data[self.const_gss_info["THIRD_TEXT"]]
            self.click_element.clickClearInput(value=self.const_step_delivery["FIRST_TEXT_AREA_VALUE"], inputText=second_text)
            self.logger.warning(f'{self.__class__.__name__} テキストを入力: 実施済み')
            self.selenium._random_sleep()

            # 保存をクリック
            self.click_element.clickElement(value=self.const_step_delivery["SAVE_BTN_VALUE"])
            self.logger.warning(f'{self.__class__.__name__} 保存をクリック: 実施済み')
            self.selenium._random_sleep()

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} 処理中にエラー発生中: {e}')

    # ----------------------------------------------------------------------------------
