const Anthropic = require('@anthropic-ai/sdk');

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

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { message } = req.body;
  if (!message || typeof message !== 'string' || message.trim().length === 0) {
    return res.status(400).json({ error: 'メッセージが空です' });
  }

  try {
    const client = new Anthropic();
    const response = await client.messages.create({
      model: 'claude-opus-4-8',
      max_tokens: 512,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: message.trim() }],
    });

    const text = response.content.find(b => b.type === 'text')?.text || '';
    res.status(200).json({ reply: text });
  } catch (err) {
    console.error('Claude API エラー:', err);
    res.status(500).json({ error: 'AIの応答取得中にエラーが発生しました。' });
  }
};
