from __future__ import annotations

import os
import logging
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ルーター（/analyze）を登録
from services.analyzer import router as analyze_router


# 設定
def _get_allowed_origins() -> List[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "").strip()
    if not raw:
        return [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",   # Vite
            "http://127.0.0.1:5173",
            "https://x.com",   # X (旧Twitter)
            "https://twitter.com",
        ]
    return [o.strip() for o in raw.split(",") if o.strip()]


APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
APP_NAME = os.getenv("APP_NAME", "SNS Checker API")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("app")


# FastAPI
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    openapi_tags=[
        {"name": "health", "description": "疎通・確認用"},
        {"name": "analyze", "description": "テキスト解析"},
    ],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(analyze_router, tags=["analyze"])



# ヘルスチェック
@app.get("/", tags=["health"])
async def root():
    return {"ok": True, "name": APP_NAME, "version": APP_VERSION}

@app.get("/health", tags=["health"])
async def health():
    return {"ok": True}

@app.get("/version", tags=["health"])
async def version():
    return {"version": APP_VERSION}