from typing import Optional
from logging import Logger, config, getLogger
import json
import datetime
from os.path import join

def get_logger(log_dir: str, json_path: str, verbose: bool=False) -> Optional[Logger]:
    """
    ロガーを取得する関数

    Args:
        log_dir (str): ログファイルを保存するディレクトリのパス
        json_path (str): ログ設定を記述したJSONファイルのパス
        verbose (bool, optional): ログレベルをDEBUGにするかどうかのフラグ。デフォルトはFalse。

    Returns:
        Optional[Logger]: ロガーオブジェクト。設定ファイルが存在しない場合や、設定ファイルの形式が不正な場合はNoneを返す。
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            log_config = json.load(f)
    except FileNotFoundError:
        print(f"設定ファイル {json_path} が見つかりません。")
        return None
    except json.JSONDecodeError:
        print(f"設定ファイル {json_path} の形式が正しくありません。")
        return None

    # ログファイル名を日付とする
    log_path = join(log_dir, f"{datetime.datetime.now().strftime('%Y%m%d')}.log")
    log_config["handlers"]["rotateFileHandler"]["filename"] = log_path

    # verbose引数が True の場合、レベルをINFOからDEBUGに置換
    if verbose:
        log_config["root"]["level"] = "DEBUG"
        log_config["handlers"]["consoleHandler"]["level"] = "DEBUG"
        log_config["handlers"]["rotateFileHandler"]["level"] = "DEBUG"

    try:
        # ロギングの設定を適用
        config.dictConfig(log_config)
    except ValueError as e:
        print(f"ログ設定の適用に失敗しました：{e}")
        return None

    # ロガーを取得
    logger = getLogger(__name__)
    return logger
