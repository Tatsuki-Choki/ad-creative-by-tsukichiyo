# Gemini API 画像生成 リファレンス

> 出典: [Gemini API - Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)

## 対応モデル

| モデル | モデルID | 特徴 |
|--------|---------|------|
| Gemini 3.1 Flash Image | `gemini-3.1-flash-image-preview` | 高速・大量処理向け |
| Gemini 3 Pro Image | `gemini-3-pro-image-preview` | プロ品質・高度な推論 |
| Gemini 2.5 Flash Image | `gemini-2.5-flash-image` | 低レイテンシ・高効率 |

## 生成モード

- **テキスト → 画像**: テキストプロンプトから画像を生成
- **テキスト + 画像 → 画像**: 既存画像をテキスト指示で編集・加工
- **マルチターン編集**: 会話形式で画像を反復的に編集
- **インターリーブ出力**: 画像と説明テキストを同時に生成

## 解像度とアスペクト比

### 対応解像度

| 解像度 | 指定値 | 備考 |
|--------|--------|------|
| 0.5K | `"512"` | Gemini 3.1 Flashのみ |
| 1K | `"1K"` | デフォルト |
| 2K | `"2K"` | |
| 4K | `"4K"` | |

※ 大文字の「K」を使用すること（`"2K"` ○ / `"2k"` ×）

### 対応アスペクト比

`1:1` `1:4` `1:8` `2:3` `3:2` `3:4` `4:1` `4:3` `4:5` `5:4` `8:1` `9:16` `16:9` `21:9`

## APIリクエスト

### Python SDK

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K"
        ),
        tools=[{"google_search": {}}]
    )
)
```

### REST API

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "プロンプト"}]}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {"aspectRatio": "16:9", "imageSize": "2K"}
    }
  }'
```

### レスポンス形式

生成画像は `inline_data` としてbase64エンコードで返される:

```json
{
  "inline_data": {
    "mimeType": "image/png",
    "data": "<BASE64_IMAGE_DATA>"
  }
}
```

## リファレンス画像

最大14枚のリファレンス画像を入力可能:

| モデル | オブジェクト画像 | キャラクター画像 |
|--------|----------------|-----------------|
| Gemini 3.1 Flash | 最大10枚 | 最大4枚 |
| Gemini 3 Pro | 最大6枚 | 最大5枚 |

## Google検索によるグラウンディング

リアルタイムデータを統合して画像生成が可能:

```python
tools=[{"google_search": {}}]
```

最新の天気、イベント、データを反映した画像を生成できる。

## 画像検索グラウンディング（3.1 Flashのみ）

```python
tools=[{
    "googleSearch": {
        "searchTypes": {
            "webSearch": {},
            "imageSearch": {}
        }
    }
}]
```

※ ソースへのクリック可能な帰属表示が必須

## Thinking（推論プロセス）

Gemini 3系モデルはデフォルトで推論プロセス（Thinking）を実行する。無効化不可。

### Thinkingレベル制御（3.1 Flash）

```python
thinking_config={
    "thinking_level": "Minimal",  # または "High"
    "include_thoughts": True
}
```

※ Thinkingトークンは表示設定に関わらず課金対象

## バッチ処理

Batch APIにより高レート制限での画像生成が可能（最大24時間のターンアラウンド）。

## 対応入力フォーマット

- `image/jpeg`
- `image/png`
- `image/gif`
- `image/webp`

## 安全性

- 全生成画像にSynthID透かしが埋め込まれる
- 著作権・知的財産権の尊重が必要
- リクエストごとにセーフティ設定が可能
