# ホロクロウラー

ホロジュールのホロライブスケジュールと Youtube の動画情報を取得して MongoDB へ登録します。

## 環境

* Windows 10 Pro 1909 x64
* Python 3.8.5 x64
* PowerShell 7.0 x64
* Visual Studio Code 1.50.0 x64
* Git for Windows 2.27.0 x64

## Poetry と pyenv の確認

```powershell
> poetry --version
Poetry version 1.1.0

> pyenv --version
pyenv 2.64.2
```

## MongoDB の確認

```powershell
> mongo --version
MongoDB shell version v4.4.1
```

## パッケージのインストール

```powershell
> poetry install
```

## Web スクレイピングのための geckodriver のダウンロード

1. geckodriver (geckodriver-v0.27.0-win64.zip) をダウンロードします。
2. geckodriver-v0.27.0-win64.zip を解凍し、geckodriver.exe を任意の場所に配置して PATH を通しておきます。

## YouTube 動画情報を取得するための YouTube Data API v3 の有効化

* Google Developer Console にログイン
* ダッシュボードでプロジェクトを作成
* ライブラリで YouTube Data API v3 を有効化
* 認証情報で認証情報を作成して APIキー を取得

## .env の作成

* .envファイルを作成する
* .env.sampleを参考にURLやAPIキーを設定する

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
