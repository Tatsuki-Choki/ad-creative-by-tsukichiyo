# Ad Creative

Meta広告用クリエイティブをAI（Gemini API `gemini-3.1-flash-image-preview`）で生成・管理するワークスペース。

## Setup

1. `.env` に Gemini API キーを設定:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
2. 依存パッケージをインストール:
   ```bash
   pip install requests
   ```

## ワークフロー（Claude Code対話型）

このディレクトリでClaude Codeを開き、**「スタート」** と入力すると、以下の5フェーズのワークフローが自動で進行します。

### Phase 1: ヒアリング
以下をヒアリングします（まとめて回答OK）:
1. クリエイティブの種類（バナー / SNS投稿 / ストーリーズ）
2. 宣伝内容（商品・サービス・キャンペーン）
3. ターゲット層（年齢・性別・興味関心）
4. トーン・雰囲気（高級感、カジュアル、信頼感 など）
5. テキスト・コピー（キャッチコピー、CTA、価格）
6. リファレンス画像（`references/` に配置）
7. 生成枚数（デフォルト: 3枚）

### Phase 2: プロンプト生成
- `brand-assets/guidelines.md` からブランド情報を読み込み
- `references/` のリファレンス画像を分析
- `docs/` のプロンプトガイド・Tipsを参照してベストプラクティスに従ったプロンプトを構築
- ユーザーに提示して調整後、`prompts/{種類}/` に保存

### Phase 3: 画像生成
```bash
python generate.py --type {banner|sns|story} --prompt "プロンプト" --count {枚数}
```
- モデル: `gemini-3.1-flash-image-preview`（日本語テキスト精度が高い）
- アスペクト比は種類に応じて自動設定（banner: 16:9, sns: 1:1, story: 9:16）
- 生成画像を `{種類}/drafts/` に保存し、ユーザーに表示
- 各画像について「採用 / 再生成 / 修正」を確認

### Phase 4: レビュー
- 「採用」画像を `{種類}/review/` に移動
- 修正が必要な場合はプロンプト調整して再生成
- 全画像が決まったらレビュー一覧を表示

### Phase 5: 承認・納品
- 最終確認後、承認画像を `{種類}/approved/` に移動
- 完了サマリー（ファイル一覧・使用プロンプト・Meta広告マネージャへのアップロード手順）を表示

## クリエイティブ種類

| 種類 | フォルダ | 用途 | 推奨サイズ | アスペクト比 |
|------|---------|------|-----------|------------|
| バナー | `banners/` | Meta フィード広告 | 1200x628px | 16:9 |
| SNS投稿 | `sns-posts/` | Meta フィード投稿 | 1080x1080px | 1:1 |
| ストーリーズ | `stories/` | Meta ストーリーズ広告 | 1080x1920px | 9:16 |

## プロンプトガイド

`docs/` に nanobanana2 の公式ドキュメント（日本語）を格納:

| ファイル | 内容 |
|---------|------|
| `docs/01_api-reference.md` | API仕様・解像度・パラメータ |
| `docs/02_prompting-guide.md` | プロンプトガイド（実践編） |
| `docs/03_prompt-tips.md` | プロンプトTips・広告向け例 |

## フォルダ構成

```
ad-creative/
├── .env                  # APIキー
├── generate.py           # 画像生成スクリプト (gemini-3.1-flash-image-preview)
├── docs/                 # nanobanana2公式ドキュメント（日本語）
│   ├── 01_api-reference.md
│   ├── 02_prompting-guide.md
│   └── 03_prompt-tips.md
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
