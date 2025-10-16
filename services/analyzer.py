from typing import Dict, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import defaultdict

from nlp.processor import tweet_diagnosis
from . import scoring
from . import gpt_cliant
import random

router = APIRouter()

# リクエスト/レスポンス定義
class AnalyzeReq(BaseModel):
    text: str = Field(..., description="解析対象テキスト", max_length=10000)

class AnalyzeRes(BaseModel):
    detail: str = Field(..., description="評価の要約説明（日本語）")
    direct_percent: float = Field(..., description="個人情報（直接）の割合％（0-100）", ge=0, le=100)
    indirect_percent: float = Field(..., description="個人情報（間接）の割合％（0-100）", ge=0, le=100)

# エンドポイント フロントに返す
@router.post("/analyze", response_model=AnalyzeRes, summary="テキスト解析（説明と割合）")
def analyze_text(req: AnalyzeReq) -> AnalyzeRes:
    tweet = req.text
    print({tweet})

    try:
        # 用意したデータを引数としてtweet_diagnosis関数に渡し、処理を実行
        nlp_result = tweet_diagnosis(tweet)
        
        # nlp_result を簡単に変更する
        
        #nlp_result_correction = {key: value[1] for key, value in nlp_result.items()}
        
        # 直接スコア計算
        direct_scores = scoring.direct_scores(nlp_result)
        # 間接スコア計算
        indirect_scores = scoring.indirect_scores(nlp_result)
        
        # 説明文 生成
        detail = gpt_cliant.gpt_function(nlp_result, direct_scores, indirect_scores)

        return AnalyzeRes(
            detail=detail,
            direct_percent=direct_scores,
            indirect_percent=indirect_scores,
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"NLP解析でエラー: {str(e)}")