# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import concurrent.futures, time
from typing import Dict, Callable, List


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


class ParallelThreadPool:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

    #!###################################################################################
    # ✅ 指定された関数を並列で実行する汎用メソッド

    def process(self, task_func: Callable, task_args_list: List, max_workers: int = 3):
        """
        concurrent.futuresは並列処理のモジュール→thread or Processかを選んで並列処理を実施できる
        future は並列処理を管理するオブジェクトであり、関数の処理結果を非同期に保持するもの
        :param task_function: 並列処理する関数（task_function(arg) の形式）
        :param task_args_list: 関数に渡す引数のリスト（例: [arg1, arg2, arg3, ...]）→ 複数の場合にはタプルで渡す(1, 10)
        :return: 各タスクの結果リスト
        """
        results = []
        count = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executer:
            # 辞書内包表記 args→複数の引数を渡したい場合にはタプルで渡す
            # executer.submitで関数を実行してfuture（関数処理を非同期で保持）を返す
            futures = {executer.submit(task_func, *args): args for args in task_args_list}

            # as_completedは関数処理が完了した結果が出たら渡す（早く処理できたものから結果を渡す）
            for future in concurrent.futures.as_completed(futures):
                task_args = futures[future]
                try:
                    result = future.result()  # 関数の戻り値を取得
                    results.append((task_args, result))
                    count += 1

                except Exception as e:
                    self.logger.error(f'{count} 回目のタスク {task_args} の処理中にエラーが発生しました: {e}')

        self.logger.info(f"全 {count} 回 並列処理、実施完了")
        return results

    #!###################################################################################
    # 並列処理の結果を出力するメソッド

    def result_write(self, results_list: List):
        for i, (arg, result) in enumerate(results_list, start=1):
            self.logger.info(f"並列処理結果 {i}回目 結果: {result} 引数: {arg}")

    #!###################################################################################
