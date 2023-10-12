import json
import datetime
from os.path import join
from logging import config, getLogger

def get_logger(log_dir, json_path, verbose=False):
    with open(json_path, "r", encoding="utf-8") as f:
        log_config = json.load(f)
    # ログファイル名を日付とする
    log_path = join(log_dir, f"{datetime.datetime.now().strftime('%Y%m%d')}.log")
    log_config["handlers"]["rotateFileHandler"]["filename"] = log_path
    # verbose引数が設定されていればレベルをINFOからDEBUGに置換
    if verbose:
        log_config["root"]["level"] = "DEBUG"
        log_config["handlers"]["consoleHandler"]["level"] = "DEBUG"
        log_config["handlers"]["rotateFileHandler"]["level"] = "DEBUG"
    # ロギングの設定を適用してロガーを取得
    config.dictConfig(log_config)
    logger = getLogger(__name__)
    #logger.addFilter(CustomFilter())
    return logger
