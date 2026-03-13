#!/usr/bin/env python3
"""
nanobanana2 画像生成スクリプト (Google Gemini API)
Usage:
    python generate.py --type banner --prompt "春セールバナー" [--count 3]
    python generate.py --type sns --prompt "新商品紹介" [--count 3]
    python generate.py --type story --prompt "キャンペーン告知" [--count 3]
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests が必要です: pip install requests")
    sys.exit(1)

# .env読み込み
ENV_PATH = Path(__file__).parent / ".env"
def load_env():
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

load_env()

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_ID = "gemini-3.1-flash-image-preview"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent"

# クリエイティブ種類 → 出力先マッピング
TYPE_MAP = {
    "banner": "banners/drafts",
    "sns": "sns-posts/drafts",
    "story": "stories/drafts",
}

# Meta広告推奨サイズ
SIZE_HINTS = {
    "banner": "1200x628px (Meta フィード広告)",
    "sns": "1080x1080px (Meta フィード投稿)",
    "story": "1080x1920px (Meta ストーリーズ)",
}

# アスペクト比マッピング
ASPECT_RATIOS = {
    "banner": "16:9",
    "sns": "1:1",
    "story": "9:16",
}


def generate_image(prompt: str, creative_type: str) -> bytes | None:
    """Gemini API経由でnanobanana2画像を生成"""
    if not API_KEY:
        print("エラー: GEMINI_API_KEY が設定されていません。.env を確認してください。")
        sys.exit(1)

    size_hint = SIZE_HINTS.get(creative_type, "")
    full_prompt = f"{prompt}\n\n推奨サイズ: {size_hint}" if size_hint else prompt

    aspect_ratio = ASPECT_RATIOS.get(creative_type, "16:9")

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
            },
        },
    }

    headers = {"Content-Type": "application/json"}
    url = f"{API_URL}?key={API_KEY}"

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"API エラー: {e}")
        return None

    data = response.json()

    # レスポンスから画像データを抽出
    for candidate in data.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                return base64.b64decode(part["inlineData"]["data"])

    print("画像データが見つかりませんでした。レスポンス:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return None


def save_image(image_data: bytes, creative_type: str, prompt: str, index: int) -> Path:
    """生成画像をdraftsフォルダに保存"""
    base_dir = Path(__file__).parent
    output_dir = base_dir / TYPE_MAP[creative_type]
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_prompt = prompt[:30].replace(" ", "_").replace("/", "_")
    filename = f"{timestamp}_{safe_prompt}_{index}.png"
    filepath = output_dir / filename

    filepath.write_bytes(image_data)
    return filepath


def main():
    parser = argparse.ArgumentParser(description="nanobanana2 画像生成 (Gemini API)")
    parser.add_argument("--type", choices=["banner", "sns", "story"], required=True, help="クリエイティブ種類")
    parser.add_argument("--prompt", required=True, help="生成プロンプト")
    parser.add_argument("--count", type=int, default=1, help="生成枚数 (デフォルト: 1)")
    args = parser.parse_args()

    print(f"生成中... (種類: {args.type}, 枚数: {args.count})")
    print(f"サイズ目安: {SIZE_HINTS.get(args.type, '未設定')}")

    for i in range(args.count):
        print(f"  [{i + 1}/{args.count}] 生成中...")
        image_data = generate_image(args.prompt, args.type)
        if image_data:
            filepath = save_image(image_data, args.type, args.prompt, i + 1)
            print(f"  [{i + 1}/{args.count}] 保存: {filepath}")
        else:
            print(f"  [{i + 1}/{args.count}] 生成失敗")

    print("完了!")


if __name__ == "__main__":
    main()
