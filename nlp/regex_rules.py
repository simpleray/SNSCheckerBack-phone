# regex_rules.py
"""
正規表現パターンを定義・利用するモジュール。

正規表現（Regex）とは:
  - 特殊な記号（メタ文字）と通常文字を組み合わせて、
    文字列のパターンを表現・検索するための仕組み。
  - 例: メールアドレス、電話番号、郵便番号の検出など。
"""

import re  # 正規表現ライブラリ


# =============================
# 正規表現パターン定義
# =============================

# 1. メールアドレス
EMAIL_PATTERN = re.compile(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    re.UNICODE
)
"""
解説:
  - [a-zA-Z0-9._%+-]+   : ユーザー名部分（1文字以上）
  - @                   : 「@」記号
  - [a-zA-Z0-9.-]+      : ドメイン名部分
  - \.                  : ドット（正規表現の . は任意文字なので、エスケープが必要）
  - [a-zA-Z]{2,}        : ドメイン末尾（例: com, jp, org）
"""


# 2. 日本の電話番号
PHONE_PATTERN = re.compile(
    r"""
    # 固定電話: 0AB-CDE-FGHI または 0AB CDEFGHI
    (?:0\d{1,4}-\d{1,4}-\d{4})|
    (?:0\d{9,10})|
    # 携帯電話: 070,080,090
    (?:0[789]0-\d{4}-\d{4})|
    (?:0[789]0\d{8})|
    # IP電話: 050
    (?:050-\d{4}-\d{4})|
    (?:050\d{8})|
    # フリーダイヤル: 0120
    (?:0120-\d{3}-\d{3})|
    (?:0120\d{6})|
    # ナビダイヤル: 0570
    (?:0570-\d{3}-\d{3})|
    (?:0570\d{6})|
    # 衛星電話・M2M等（020,0200）
    (?:020\d{8,10})
    """,
    re.VERBOSE
)
"""
例: 
  - 090-1234-5678
  - 03-1234-5678
  - 0120-123-456
注意:
  - 存在しない番号形式もマッチする可能性あり
  - 厳密にするには総務省の番号計画に基づく先頭番号制限を追加可能
"""


# 3. 日本の郵便番号（7桁）
POSTAL_PATTERN = re.compile(
    r'\d{3}-\d{4}|\d{7}',
    re.UNICODE
)
"""
例:
  - 123-4567
  - 1234567
"""


# =============================
# 検出関数群
# =============================

def extract_emails(text: str):
    """文章からすべてのメールアドレスを抽出して返す"""
    return EMAIL_PATTERN.findall(text)


def extract_phones(text: str):
    """文章からすべての電話番号を抽出して返す"""
    return PHONE_PATTERN.findall(text)


def extract_postals(text: str):
    """文章からすべての郵便番号を抽出して返す"""
    return POSTAL_PATTERN.findall(text)


def extract_all(text: str):
    """
    メール・電話番号・郵便番号をまとめて抽出し、
    件数が1以上のものだけ返す
    """
    emails = extract_emails(text)
    phones = extract_phones(text)
    postals_raw = extract_postals(text)

    # 郵便番号と電話番号が重複する場合 → 電話番号を優先
    postals = [
        p for p in postals_raw
        if all(
            re.sub(r"\D", "", p) not in re.sub(r"\D", "", phone)
            for phone in phones
        )
    ]

    # 件数1以上のものだけ辞書に追加
    result = {}
    if len(emails) > 0:
        result["emails"] = emails
        result["emails_count"] = len(emails)
    if len(phones) > 0:
        result["phones"] = phones
        result["phones_count"] = len(phones)
    if len(postals) > 0:
        result["postals"] = postals
        result["postals_count"] = len(postals)

    return result if result else None
