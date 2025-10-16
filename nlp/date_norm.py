# date_norm.py
"""
テキスト中の日時表現（例: 「明日」「来週」「毎週金曜日」など）を
ISO形式に正規化するモジュール。

同時に以下の情報も返す:
- 未来の日時かどうか
- 繰り返しの予定かどうか
- 祝日に該当するかどうか
"""

# =============================
# ライブラリ読み込み
# =============================
import re
import csv
import dateparser
from dateutil import parser              # ISO形式の解析
from dateutil.relativedelta import relativedelta  # 日付の加減算
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo            # タイムゾーン対応

# =============================
# 補足説明
# =============================
"""
timedelta:
    - 時間の差（期間）を表現するクラス
    - days, hours, minutes, seconds, weeks を指定可能
    - datetime に加算・減算して未来や過去を計算できる
    例: timedelta(days=1, hours=2, minutes=30)
        → 1日2時間30分
"""

# =============================
# 日本語→英語の変換辞書
JP_TO_EN = {
    "今日": "today",
    "明日": "tomorrow",
    "明後日": "day after tomorrow",
    "明々後日": "in three days",
    "昨日": "yesterday",
    "一昨日": "two days ago",
    "今週": "this week",
    "来週": "next week",
    "再来週": "week after next",
    "先週": "last week",
    "先々週": "two weeks ago",
    "今月": "this month",
    "来月": "next month",
    "再来月": "month after next",
    "先月": "last month",
    "先々月": "two months ago",
    "今年": "this year",
    "来年": "next year",
    "再来年": "year after next",
    "去年": "last year",
    "一昨年": "two years ago",
}

# =============================
# タイムゾーン設定
# =============================
JST = ZoneInfo("Asia/Tokyo")

# =============================
# 祝日データの読み込み
# =============================
HOLIDAYS = []
try:
    # プロジェクト直下に "syukujitsu.csv" を配置する想定
    with open("syukujitsu.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # CSV の 1列目に日付 (YYYY-MM-DD) がある前提
            HOLIDAYS.append(row[0])
except FileNotFoundError:
    # ファイルが無い場合は仮のデータ
    HOLIDAYS = ["祝日がありませんでした"]

# =============================
# 日時正規化関数（祝日対応版）
# =============================
def normalize_datetime(text, now_iso=None):
    now = datetime.now(JST) if now_iso is None else parser.isoparse(now_iso)

    # 日本語を英語に変換（辞書にない場合はそのまま）
    en_text = JP_TO_EN.get(text, text)

    # dateparser で解析
    parsed = dateparser.parse(
        en_text,
        settings={
            "TIMEZONE": "Asia/Tokyo",
            "RETURN_AS_TIMEZONE_AWARE": True,
            "RELATIVE_BASE": now,
            "PREFER_DATES_FROM": "future"
        }
    )

    if parsed is None:
        return None

    return {
        "date": text,
        "iso": parsed.isoformat(),
        "is_future": parsed > now,
        "is_repeated": False,
        "in_holiday": parsed.date().isoformat() in HOLIDAYS
    }
