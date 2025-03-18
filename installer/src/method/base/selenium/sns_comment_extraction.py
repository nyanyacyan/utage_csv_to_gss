# coding: utf-8

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pandas as pd
from datetime import datetime
from typing import List
from youtube_comment_downloader import YoutubeCommentDownloader
import snscrape.modules.twitter as sntwitter

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.utils.path import BaseToPath
from method.base.decorators.decorators import Decorators
from method.base.utils.fileWrite import FileWrite

decoInstance = Decorators()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# ファイルに書き込みする基底クラス


class YoutubeComment:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.path = BaseToPath()
        self.file_write = FileWrite()
        self.currentDate = datetime.now().strftime("%m%d")

    # ----------------------------------------------------------------------------------
    # youtubeComment

    def process(self, url: str, file_name: str):
        df = self._comment_downloader(url=url)
        self._change_df_to_excel(df=df, file_name=file_name)

    # ----------------------------------------------------------------------------------
    # youtubeコメントダウンロード

    def _comment_downloader(self, url: str):
        downloader = YoutubeCommentDownloader()
        comments = downloader.get_comments_from_url(url)

        comment_data = []
        for comment in comments:
            comment_data.append({
                "コメント本文": comment.get("text"),
                "投稿時間": comment.get("time"),
                "投稿者": comment.get("author"),
                "いいね": comment.get("votes"),
                "ハート": comment.get("heart"),
                "url": url
            })

        # DataFrame に変換
        df = pd.DataFrame(comment_data)
        df.index += 1  # index を1始まりにする
        df.index.name = "index"

        self.logger.debug(f'コメントDataFrame:\n{df.head()}')

        return df
    # ----------------------------------------------------------------------------------

    def _change_df_to_excel(self, df: pd.DataFrame, file_name):
        output_file_path = self.path.getWriteFilePath(fileName=file_name)
        df.to_excel(output_file_path, index=True)

    # ----------------------------------------------------------------------------------

# **********************************************************************************
# ファイルに書き込みする基底クラス


class XComment:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.path = BaseToPath()
        self.file_write = FileWrite()
        self.currentDate = datetime.now().strftime("%m%d")

    # ----------------------------------------------------------------------------------
    # youtubeComment

    def process(self, user_name: str, tweet_id: str, file_name: str):
        df = self._download_comment_data(user_name=user_name, tweet_id=tweet_id)
        self._change_df_to_excel(df=df, file_name=file_name)

    # ----------------------------------------------------------------------------------


    def _download_comment_data(self, user_name: str, tweet_id: str):
        try:
            query = f"to:{user_name} conversation_id:{tweet_id}"
            tweets = []
            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                print("取得成功:", tweet.content)
                tweets.append({
                    "表示名": tweet.user.displayname,
                    "コメント本文": tweet.content,
                    "投稿日時": tweet.date,
                    "投稿者": tweet.user.username,
                    "いいね": tweet.likeCount,
                    "リツイート数": tweet.retweetCount,
                    "リプライ数": tweet.replyCount,
                    "tweet ID": tweet.id,
                    "URL": tweet.url
                })
            # DataFrame に変換
            df = pd.DataFrame(tweets)
            df.index += 1  # index を1始まりにする
            df.index.name = "index"

            self.logger.debug(f'コメントDataFrame:\n{df.head()}')
            return df

        except Exception as e:
            self.logger.error(f'{self.__class__.__name__} _download_comment_data: 処理中にエラーが発生{e}')
            raise

    # ----------------------------------------------------------------------------------

    def _change_df_to_excel(self, df: pd.DataFrame, file_name):
        output_file_path = self.path.getWriteFilePath(fileName=file_name)
        df.to_excel(output_file_path, index=True)

    # ----------------------------------------------------------------------------------

#youtube
if __name__ == "__main__":
    currentDate = datetime.now().strftime("%m%d")

    url = "https://twitter.com/wannyanheiwa/status/1897935573702393976"
    last_five = url[-5:]
    post_date = "0308"

    user_name = "wannyanheiwa"
    tweet_id = "1897935573702393976"


    # file_name = f"youtube_comments{post_date}-{last_five}.xlsx"
    file_name = f"X_comments{post_date}-{last_five}.xlsx"


    # youtube_comment = YoutubeComment()
    # youtube_comment.process(url=url, file_name=file_name)

    X_comment = XComment()
    X_comment.process(user_name=user_name, tweet_id=tweet_id, file_name=file_name)
