/* ===== チャットボット FAQ ロジック ===== */

// FAQ データ: キーワード配列と対応する回答
const FAQ = [
  {
    keywords: ['営業', '時間', '定休', '休み', '何時', 'いつ'],
    answer: '営業時間は 10:00〜20:00 です。定休日は毎週月曜日となっております。'
  },
  {
    keywords: ['メニュー', '料金', '値段', '価格', 'カット', 'カラー', 'トリートメント'],
    answer: 'カット ¥4,000〜、カラー ¥8,000〜、トリートメント ¥3,000〜 となっております。詳しくはページ内「サービス」欄をご確認ください。'
  },
  {
    keywords: ['予約', '申し込み', '申込', 'ブック', 'book'],
    answer: 'ご予約はページ内「お問い合わせ」フォーム、またはお電話（000-0000-0000）にて承っております。'
  },
  {
    keywords: ['アクセス', '場所', '住所', '駐車場', '駐車', '駅', '行き方'],
    answer: '〇〇駅より徒歩5分です。駐車場は2台分ご用意しております（無料）。'
  }
];

// メッセージを表示する関数
function appendMessage(text, type) {
  const box = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = `msg msg-${type}`;
  div.textContent = text;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

// ユーザーの入力に対して FAQ を検索して回答する
function handleInput() {
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;

  appendMessage(text, 'user');
  input.value = '';

  // キーワードマッチング
  const matched = FAQ.find(faq =>
    faq.keywords.some(kw => text.includes(kw))
  );

  // 少し遅延を入れて返答を自然に見せる
  setTimeout(() => {
    const reply = matched
      ? matched.answer
      : 'ご質問ありがとうございます。詳しくはお電話（000-0000-0000）またはお問い合わせフォームよりお気軽にご連絡ください。';
    appendMessage(reply, 'bot');
  }, 400);
}

// チャットウィンドウの開閉
function toggleChat() {
  const win = document.getElementById('chat-window');
  win.classList.toggle('open');

  // 初回オープン時にウェルカムメッセージを表示
  const messages = document.getElementById('chat-messages');
  if (win.classList.contains('open') && messages.children.length === 0) {
    appendMessage('こんにちは！ご質問をどうぞ。「営業時間」「料金」「予約」「アクセス」などについてお答えできます。', 'bot');
  }
}

// Enter キーで送信
document.getElementById('chat-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') handleInput();
});

// スクロールフェードイン
const observer = new IntersectionObserver(
  entries => entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  }),
  { threshold: 0.15 }
);

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

// モバイルナビの開閉
const toggle = document.getElementById('nav-toggle');
const nav = document.getElementById('main-nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => nav.classList.toggle('open'));
}
