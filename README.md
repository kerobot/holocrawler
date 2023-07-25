# ホロクロウラー

ホロジュールのホロライブスケジュールと Youtube の動画情報を取得して MongoDB へ登録します。

## 環境

* Windows 11
* Python 3.11
* PowerShell 7.3
* Visual Studio Code 1.80
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

## Web スクレイピングのために google-chrome と chromedriver を導入

※ Windowsの場合はchromedriver.exeを配置する

```bash
cd /tmp
wget https://dl.google.com/linux/linux_signing_key.pub
sudo apt-key add linux_signing_key.pub
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt -f install -y
sudo apt install google-chrome-stable
google-chrome --version
sudo apt install chromium-chromedriver
chromedriver -v
which chromedriver
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

## pyproject.toml を利用して Python のパッケージを一括インストール

```powershell
> python -m venv .venv
> poetry install
```

## lounch.json の作成

```json
{
    "version": "0.2.0",
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

## プログラムの実行

```powershell
> poetry run python main.py --csvpath c:\temp\test.csv
```
