from typing import Dict, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import defaultdict
import test_gpt


router = APIRouter()

"""
# リクエスト/レスポンス定義
class AnalyzeReq(BaseModel):
    text: str = Field(..., description="解析対象テキスト", max_length=10000)

class AnalyzeRes(BaseModel):
    detail: str = Field(..., description="評価の要約説明（日本語）")
    direct_percent: float = Field(..., description="個人情報（直接）の割合％（0-100）", ge=0, le=100)
    indirect_percent: float = Field(..., description="個人情報（間接）の割合％（0-100）", ge=0, le=100)
"""


    # tweet = input("解析対象テキストを入力してください: ")
        # 用意したデータを引数としてtweet_diagnosis関数に渡し、処理を実行
nlp_result = {'age': [['23歳'], 1],
    'date': [[{'date': '昨日',
            'in_holiday': False,
            'is_future': False,
            'is_repeated': False,
            'iso': '2025-08-16T12:00:00+09:00'}],
            1],
    'email': [['kensuke.k@example.com'], 1],
    'person': [['幸田健介'], 1],
    'phone': [['080-1234-5678'], 1],
    'place': [['東京都千代田区丸の内'], 1]}
    
direct_scores = 99
indirect_scores = 0
    

    # 説明文 生成
detail = test_gpt.gpt_function(nlp_result, direct_scores, indirect_scores)

print(detail )