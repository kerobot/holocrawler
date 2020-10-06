> poetry --version
Poetry version 1.1.0

> pyenv --version
pyenv 2.64.2

---

> poetry new holocrawler --name app

> cd holocrawler

> pyenv update

> pyenv install -l

> pyenv local 3.8.5

> pyenv rehash

> poetry add pylint
> poetry add beautifulsoup4
> poetry add requests
> poetry add selenium
> poetry add lxml
> poetry add google-api-python-client
> poetry add python-dotenv
> poetry add python-dotenv
> poetry add pymongo

> poetry run python -V
Python 3.8.5

> python -V
Python 3.8.5

---

git 初期化
git init

--

Webスクレイピングのための geckodriver のダウンロード
geckodriver(geckodriver-v0.26.0-win64.zip)をダウンロードする。
geckodriver-v0.26.0-win64.zipを解凍し、geckodriver.exeをプロジェクトルートに配置する。

--

.env の作成
.envファイルを作成する
.env.sampleを参考にURLや接続文字列を設定する

--

.gitignore の作成
__pycache__
/venv/
/geckodriver.log
/geckodriver.exe
.env

--

MongoDB への接続を確認
データベース holoduledb に対してアクセス権を設定しておく
mongo localhost:27017/admin -u admin -p
use holoduledb
db.createUser( { user:"owner", pwd:"password", roles:[{ "role" : "dbOwner", "db" : "holoduledb" }] } );
コレクション holodules を作成しておく
db.createCollection("holodules");

mongo
use holoduledb
db.auth("user", "password");
db.createCollection("holodules");
show collections

---

launch.json を作成してデバッグ実行
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}
