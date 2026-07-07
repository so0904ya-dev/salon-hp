# TikTok投稿ガイド（猫の料理動画）

## 1. 動画を生成する

```bash
pip install google-genai
export GEMINI_API_KEY="あなたのGemini APIキー"
python generate_cat_cooking_video.py
```

成功すると `cat_cooking.mp4` が作成されます。

- Gemini APIキーは https://aistudio.google.com/apikey から取得します。
- Veo（動画生成）は有料枠が必要な場合があります。料金は事前に確認してください。

## 2. TikTokに投稿する方法（2つの選択肢）

### A. 手動でアップロード（最も簡単・おすすめ）

1. TikTokアプリ／Webで通常通りログイン
2. `cat_cooking.mp4` を選択して投稿
3. キャプション・ハッシュタグ（例: #猫 #cooking #AI動画）を付けて公開

→ APIの審査が不要で、今すぐできます。

### B. TikTok Content Posting API で自動投稿

自動化したい場合は本物のAPI連携が必要ですが、以下の制約があります。

- TikTok for Developers (https://developers.tiktok.com) でアプリ登録が必要
- Content Posting API の利用には**TikTokによる審査・承認**が必要（個人利用でも申請が必要な場合あり）
- OAuth認可フローでユーザー自身のTikTokアカウントとの連携が必要
- 投稿頻度・コンテンツポリシーの制限あり

このステップは登録者本人（あなた）がTikTok Developerポータルで行う必要があり、私が代行することはできません。承認が済んでアクセストークンが発行された後であれば、アップロード用のスクリプトを追加で作成できます。

## 3. 収益化について

TikTokでの収益化（Creator Rewards Program等）には、フォロワー数・動画再生数などの条件があります。最新の条件はTikTok公式の規約を確認してください。AI生成コンテンツであることの開示が必要な場合があるため、TikTokのAIコンテンツ表示ポリシーも事前に確認することをおすすめします。
