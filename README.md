# ホロクロウラー

ホロジュールのホロライブスケジュールと Youtube の動画情報を取得して MongoDB へ登録します。

## 環境

* Windows 11
* Python 3.11
* PowerShell 7.3.8
* Visual Studio Code 1.83
* Git for Windows 2.41

## Poetry と pyenv の確認

```powershell
> poetry --version
Poetry version 1.3.2

> pyenv --version
pyenv 3.1.1
```

## MongoDB の確認

```powershell
> mongosh --version
1.6.0
```

## MongoDB に接続できることを確認

```powershell
> mongosh localhost:27017/admin -u admin -p
```

## データベースを作成してロール（今回は dbOwner ）を設定

```powershell
MongoDB > use holoduledb
MongoDB > db.createUser( { user:"owner", pwd:"password", roles:[{ "role" : "dbOwner", "db" : "holoduledb" }] } );
```

## Web API からアクセスする際のユーザー情報を登録（参考）

```powershell
MongoDB > db.createCollection("users");
MongoDB > db.users.save( {"id":"1", "username":"dummy", "password":"dummy", "firstname":"dummy", "lastname":"dummy"} );
MongoDB > db.users.find();
```

## Web スクレイピングのために google-chrome と chromedriver を導入

※ Windows の場合

最新の Google Chrome をインストールしておく

※ Ubuntu の場合

```bash
cd /tmp
wget https://dl.google.com/linux/linux_signing_key.pub
sudo apt-key add linux_signing_key.pub
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt -f install -y
sudo apt install google-chrome-stable
google-chrome --version

# chromedriver のインストールは不要（Selenium 4.6 から、Selenium自体にChromeDriver自動更新機能「Selenium Manager」が搭載されたため）
# sudo apt install chromium-chromedriver
# chromedriver -v
# which chromedriver
```

## YouTube 動画情報を取得するための YouTube Data API v3 を有効化して API キーを取得

※ [Google Developer Console](https://console.developers.google.com/?hl=JA)

* Google Developer Console にログイン
* ダッシュボードでプロジェクトを作成
* ライブラリで YouTube Data API v3 を有効化
* 認証情報で認証情報を作成して APIキー を取得

## .envファイルを作成し、URLやAPIキーを設定

* .envファイルを作成する
* .env.sampleを参考にURLやAPIキーを設定する

## プロジェクトで利用する Python をインストール

```powershell
> pyenv install 3.11.1
```

## プロジェクトで利用するローカルの Python のバージョンを変更

```powershell
> pyenv local 3.11.1
> python -V
Python 3.11.1
```

## バージョンを指定して、Python 仮想環境を作成

```powershell
> poetry env use python311
> または python -m venv .venv
```

## pyproject.toml を利用して Python のパッケージを一括インストール

```powershell
> poetry install
```

## プログラムの実行

```powershell
> poetry run python main.py --csvpath c:\temp\test.csv
```

## lounch.json の設定

```json
{
    "version": "1.0.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "args": ["--csvpath","c:\\temp\\holodule.csv"]
        }
    ]
}
```
