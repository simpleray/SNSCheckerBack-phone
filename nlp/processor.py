# processor.py

import sys, os, traceback, pprint,dateparser
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import defaultdict
from .regex_rules import extract_all       # 正規表現でメール/電話/郵便番号を抽出する関数
from .date_norm import normalize_datetime  # DATE表現をISO形式に正規化する関数
from .gazeteer import lookup_place         # 場所名をカテゴリ/規模に正規化する関数
from .pipeline import get_nlp              # spaCyのNLPモデルを取得する関数


# ===== 定数 =====
# 日付正規化の基準となる日時 (ここでは2025年8月17日12時を基準時刻とする)
BASE_ISO = datetime(2025, 8, 17, 12, 0, tzinfo=ZoneInfo("Asia/Tokyo")).isoformat()

# 場所に関するエンティティラベルの一覧 (spaCyやカスタムモデルが出力するラベル)
PLACE_LABELS = ["GPE", "Province", "FAC", "City", "ORG", "GOE_Other", "Organization_Other","station", "hospital"]
# 数字に関するエンティティラベル (カスタムNERが出力するラベル)



# ===== ユーティリティ =====
def pretty_print(title, data):
    """見やすい形で結果を出力するヘルパー関数"""
    print("\n" + "="*60)   # 区切り線
    print(title)           # タイトル
    print("="*60)          # 区切り線
    pprint.pprint(data)    # データを見やすく整形して出力


# ===== 処理 =====


def analyze_entities(tweet, nlp):
    """spaCyを使って固有表現抽出を行い、ラベルごとにまとめる"""
    doc = nlp(tweet)                  # NLP解析を実行
    entities = defaultdict(list)     # ラベルごとにリストを保持
    for ent in doc.ents:             # doc.ents = 抽出されたエンティティ一覧
        entities[ent.label_].append(ent.text)  # ラベルをキーにしてテキストを追加
    return entities


def extract_contacts(tweet):
    """テキストからメール・電話番号・郵便番号を抽出する"""
    if not tweet:
        return None  # テキストが空の場合はNoneを返す
    return extract_all(tweet)


def normalize_dates(entities):
    """DATEエンティティをISO形式に正規化する"""
    results = []
    for date_tweet in entities.get("DATE", []):   # DATEラベルがある場合のみ処理
        norm = normalize_datetime(date_tweet, now_iso=BASE_ISO)  # 正規化
        results.append((date_tweet, norm))
        if not results:
                return None     
        else: return results        # 元テキストと正規化結果をタプルで保存
    


def normalize_places(entities):
    """場所エンティティを gazeteer を使ってカテゴリ/規模に正規化する"""
    results = []
    for label in PLACE_LABELS:                        # 場所関連のラベルを順番に確認
        for place_tweet in entities.get(label, []):    # そのラベルに属するテキストを取り出す
            norm = lookup_place(place_tweet)           # gazeteer辞書を使って正規化
            results.append((place_tweet, norm))  
            
            if not results:
                return None     
            else: return results

def build_result_dict(entities, contacts, normalized_dates, normalized_places):
    """
    抽出・正規化された結果を指定のフォーマットで辞書にまとめる
    """
    results = {}

    # 1. person（SpaCyが抽出した "Person" ラベルを格納）
    persons = entities.get("Person", [])
    if persons:
        results["person"] = [persons, len(persons)]

    # 2. age（カスタムNERで "Age" ラベルを格納）
    ages = entities.get("Age", [])
    # '-' を含むものは除外
    valid_ages = [age for age in ages if "-" not in age]
    if valid_ages:
        results["age"] = [valid_ages, len(valid_ages)]


    # 3. date（正規化日付を格納）
    if normalized_dates:
        norm_dates = [norm for _, norm in normalized_dates]
        if norm_dates:
            results["date"] = [norm_dates, len(norm_dates)]

    # 4. contacts（メール・電話・郵便番号を格納）
    if contacts:
        if contacts.get("emails"):
            results["email"] = [contacts["emails"], len(contacts["emails"])]
        if contacts.get("phones"):
            results["phone"] = [contacts["phones"], len(contacts["phones"])]
        if contacts.get("postals"):
            results["postal"] = [contacts["postals"], len(contacts["postals"])]

    # 5. places（場所の正規化結果をカテゴリごとに格納）
    if normalized_places:
        stations, hospitals, spots, unknowns = [], [], [], []
        for tweet, norm in normalized_places:
            cat = norm["category"]
            if cat == "駅":
                stations.append(tweet)
            elif cat == "病院":
                hospitals.append(tweet)
            elif cat == "観光地":
                spots.append(tweet)
            elif cat == "不明":
                unknowns.append(tweet)

        if stations:
            results["station"] = [stations, len(stations)]
        if hospitals:
            results["hospital"] = [hospitals, len(hospitals)]
        if spots:
            results["tourristspot"] = [spots, len(spots)]
        if unknowns:
            results["place"] = [unknowns, len(unknowns)]

    return results




def tweet_diagnosis(tweet):
    """全体の処理の流れをまとめた関数"""

    try:
        # NLP解析で固有表現を抽出
        nlp = get_nlp()
        entities = analyze_entities(tweet, nlp)
    except Exception:
        print("NLP解析でエラーが発生しました")
        traceback.print_exc()
        return {}
    pretty_print("抽出された固有表現", entities)

    # メール/電話/郵便番号の抽出
    contacts = extract_contacts(tweet)

    # DATEの正規化
    normalized_dates = normalize_dates(entities)

    # 場所の正規化
    normalized_places = normalize_places(entities)

    # 新しい辞書にまとめる
    final_results = build_result_dict(entities, contacts, normalized_dates, normalized_places)

    # 表示
    pretty_print("最終結果", final_results)

    return final_results

