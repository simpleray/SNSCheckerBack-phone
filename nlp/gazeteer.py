# gazetteer.py
"""
地名・施設名を管理するモジュール。
CSVファイルから「学校」「駅」「病院」などの名前を読み込み、
カテゴリ・規模（大規模/小規模）を付与して検索できるようにする。
"""

import csv
from rapidfuzz import fuzz

# =============================
# グローバル変数
# =============================
PLACES = []  # 全施設データを格納


# =============================
# CSV 読み込み関数
# =============================
def load_csv(file_path, category):
    """
    指定した CSV ファイルを読み込み、PLACES に追加する。

    Parameters
    ----------
    file_path : str
        CSV ファイルのパス
    category : str
        「学校」「駅」「病院」などのカテゴリ

    Notes
    -----
    ・学校 → 小規模固定
    ・病院 → 小規模固定
    ・駅   → 大規模固定
    ・観光地  → 大規模固定
    """
    SIZE_MAP = {
        "学校": "小規模",
        "病院": "小規模",
        "駅": "大規模",
        "観光地": "大規模"
    }
    size_fixed = SIZE_MAP.get(category, "大規模")  # デフォルトは小規模

    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name = row[0]  # CSVの1列目が施設名と想定
                PLACES.append({
                    "name": name,
                    "category": category,
                    "size": size_fixed
                })
    except FileNotFoundError:
        print(f"[ERROR] {file_path} が見つかりません。")


# =============================
# CSV データ読み込み（初期化）
# =============================
load_csv("data/schools.csv", "学校")
load_csv("data/stations.csv", "駅")
load_csv("data/hospital.csv", "病院")
load_csv("data/touristspots.csv", "観光地")  # 観光地も追加


# =============================
# 場所検索関数
# =============================
# =============================
# 場所検索関数（完全一致 → 部分一致 → 類似度で選出）
# =============================
def lookup_place(name):
    """
    名前からカテゴリと規模を返す。

    処理の流れ
    1. 完全一致で検索
    2. 完全一致がなければ部分一致で候補リスト作成
    3. 複数候補がある場合は RapidFuzz 類似度で最適候補を返す
    4. 一致が無ければ {"category": "不明", "size": None} を返す
    """

    # 1. 完全一致検索
    for place in PLACES:
        if place["category"] == "駅":
            if name == place["name"]:
                return {"category": place["category"]}

        elif place["category"] == "病院":
            if name == place["name"]:
                return {"category": place["category"]}

        elif place["category"] == "観光地":
            if name == place["name"]:
                return {"category": place["category"]}

        elif place["category"] == "学校":
            if name == place["name"]:
                return {"category": place["category"]}

    # 2. 部分一致候補リスト作成
    candidates = []
    for place in PLACES:
        if place["category"] == "駅":
            if name.endswith("駅") and place["name"] in name:
                candidates.append(place)

        elif place["category"] == "病院":
            if place["name"] in name or name in place["name"]:
                candidates.append(place)

        elif place["category"] == "観光地":
            if place["name"] in name or name in place["name"]:
                candidates.append(place)

        elif place["category"] == "学校":
            if place["name"] in name or name in place["name"]:
                candidates.append(place)

        else:
            if place["name"] in name:
                candidates.append(place)

    # 3. 候補がある場合
    if candidates:
        best_place = max(candidates, key=lambda p: fuzz.ratio(name, p["name"]))
        return {"category": best_place["category"]}

    # 4. 一致がない場合は "不明" を返す
    return {"category": "不明"}
