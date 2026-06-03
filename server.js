import express from 'express';
import Anthropic from '@anthropic-ai/sdk';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const client = new Anthropic(); // ANTHROPIC_API_KEY を環境変数から読み込む

app.use(express.json());
app.use(express.static(__dirname)); // HTML/CSS/JS を配信

// チャットボット用システムプロンプト
const SYSTEM_PROMPT = `あなたは美容サロン「SalonName」のAIアシスタントです。
お客様のご質問に対して丁寧に日本語でお答えください。

【サロン情報】
- 営業時間: 10:00〜20:00
- 定休日: 毎週月曜日
- 所在地: 〇〇県〇〇市〇〇町1-2-3（〇〇駅より徒歩5分）
- 駐車場: 2台分（無料）
- 電話番号: 000-0000-0000
- 予約方法: お電話またはお問い合わせフォームより承っております

【メニュー・料金】
- カット: ¥4,000〜
- カラー: ¥8,000〜
- トリートメント: ¥3,000〜
- パーマ: ¥9,000〜

サロンに関係のないご質問には「申し訳ございませんが、サロンに関するご質問のみお答えしております」とお伝えください。
回答は簡潔に3文以内でまとめてください。`;

// POST /api/chat — ストリーミングで Claude に問い合わせ
app.post('/api/chat', async (req, res) => {
  const { message } = req.body;
  if (!message || typeof message !== 'string' || message.trim().length === 0) {
    return res.status(400).json({ error: 'メッセージが空です' });
  }

  // SSE ヘッダーを設定
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  try {
    const stream = client.messages.stream({
      model: 'claude-opus-4-8',
      max_tokens: 512,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: message.trim() }],
    });

    // テキストデルタをクライアントへ順次送信
    stream.on('text', (delta) => {
      res.write(`data: ${JSON.stringify({ delta })}\n\n`);
    });

    await stream.finalMessage();
    res.write('data: [DONE]\n\n');
    res.end();
  } catch (err) {
    console.error('Claude API エラー:', err);
    res.write(`data: ${JSON.stringify({ error: 'AIの応答取得中にエラーが発生しました。' })}\n\n`);
    res.end();
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`サーバー起動: http://localhost:${PORT}`);
});
