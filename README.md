# Ad Creative

## Setup

1. `.env` に Gemini API キーを設定:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
2. 依存パッケージをインストール:
   ```bash
   pip install requests
   ```

## ワークフロー (Claude Code)

### Step 1: 準備
- `brand-assets/` にロゴ・カラーガイドラインを格納
- `references/` にリファレンス画像を収集

### Step 2: プロンプト作成
Claude Codeに指示してプロンプトを生成・保存:
```
「references/ の画像を参考に、春セール用のバナープロンプトを作成して」
```
→ `prompts/banners/` にテンプレート保存

### Step 3: 画像生成
Claude Codeから直接実行:
```bash
python generate.py --type banner --prompt "春セールバナー" --count 3
```
または Claude Code に「バナーを3枚生成して」と指示

### Step 4: 社内レビュー
- Claude Codeに `drafts/` の画像を確認させて選定
- 採用候補を `review/` に移動

### Step 5: 承認・納品
- 承認済み素材を `approved/` に移動

## クリエイティブ種類

| 種類 | フォルダ | 用途 | 推奨サイズ |
|------|---------|------|-----------|
| バナー | `banners/` | Meta フィード広告 | 1200x628px |
| SNS投稿 | `sns-posts/` | Meta フィード投稿 | 1080x1080px |
| ストーリーズ | `stories/` | Meta ストーリーズ広告 | 1080x1920px |

## Meta広告 サイズ規定

| 配置 | 推奨サイズ | アスペクト比 | 備考 |
|------|-----------|-------------|------|
| フィード | 1080x1080px | 1:1 | 正方形、最も汎用的 |
| フィード (横長) | 1200x628px | 1.91:1 | リンク広告向け |
| ストーリーズ/リール | 1080x1920px | 9:16 | フルスクリーン |
| 右カラム | 1200x1200px | 1:1 | デスクトップのみ |

## フォルダ構成

```
ad-creative/
├── .env                  # APIキー
├── generate.py           # 画像生成スクリプト
├── brand-assets/         # ブランド素材
│   ├── logos/
│   └── guidelines.md
├── references/           # リファレンス画像
├── prompts/              # プロンプトテンプレート
│   ├── banners/
│   ├── sns-posts/
│   └── stories/
├── banners/              # バナー広告
│   ├── drafts/           # 生成物
│   ├── review/           # レビュー中
│   └── approved/         # 承認済み
├── sns-posts/            # SNS投稿画像
│   ├── drafts/
│   ├── review/
│   └── approved/
└── stories/              # ストーリーズ広告
    ├── drafts/
    ├── review/
    └── approved/
```
