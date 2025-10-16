#仮想環境の構築
py -3.11 -m venv .venv

#仮想環境の実行
./.venv/Scripts/Activate.ps1

#使用されているimportをまとめてダウンロード
pip install -r .\requirements.txt

#開発サーバーの起動コマンド
fastapi dev --port 8080