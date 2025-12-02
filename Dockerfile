# ベースイメージ
FROM python:3.10-slim

# 作業ディレクトリ
WORKDIR /app

# 依存関係のコピー
COPY requirements.txt .

# ライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体をコピー
COPY . .

# Flask を外部からアクセスできるように
ENV PORT=8080
EXPOSE 8080

# 起動コマンド（app.py に合わせて修正）
CMD ["python", "app.py"]
