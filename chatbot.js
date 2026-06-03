/* ===== AI チャットボット — Claude API 連携版 ===== */

// メッセージを表示する関数
function appendMessage(text, type) {
  const box = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = `msg msg-${type}`;
  div.textContent = text;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
  return div;
}

// タイピングインジケーターを表示
function showTyping() {
  const box = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = 'msg msg-bot typing-indicator';
  div.id = 'typing-indicator';
  div.textContent = '入力中…';
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

// タイピングインジケーターを削除
function hideTyping() {
  const el = document.getElementById('typing-indicator');
  if (el) el.remove();
}

// Claude API にメッセージを送信してストリーミング受信
async function sendToClaude(userText) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userText }),
  });

  if (!response.ok) {
    throw new Error('サーバーエラー');
  }

  // SSE をストリーミングで処理
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let botDiv = null;
  let buffer = '';

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop(); // 未完結の行は次ループへ持ち越す

    for (const line of lines) {
      if (!line.startsWith('data: ')) continue;
      const payload = line.slice(6).trim();
      if (payload === '[DONE]') break;

      try {
        const { delta, error } = JSON.parse(payload);
        if (error) {
          hideTyping();
          appendMessage(error, 'bot');
          return;
        }
        if (delta) {
          if (!botDiv) {
            hideTyping();
            botDiv = appendMessage('', 'bot');
          }
          botDiv.textContent += delta;
          const box = document.getElementById('chat-messages');
          box.scrollTop = box.scrollHeight;
        }
      } catch (_) {
        // JSON パース失敗は無視
      }
    }
  }
}

// ユーザーの入力を処理
async function handleInput() {
  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send');
  const text = input.value.trim();
  if (!text) return;

  appendMessage(text, 'user');
  input.value = '';
  input.disabled = true;
  sendBtn.disabled = true;

  showTyping();

  try {
    await sendToClaude(text);
  } catch {
    hideTyping();
    appendMessage('通信エラーが発生しました。しばらくしてからお試しください。', 'bot');
  } finally {
    input.disabled = false;
    sendBtn.disabled = false;
    input.focus();
  }
}

// チャットウィンドウの開閉
function toggleChat() {
  const win = document.getElementById('chat-window');
  win.classList.toggle('open');

  // 初回オープン時にウェルカムメッセージを表示
  const messages = document.getElementById('chat-messages');
  if (win.classList.contains('open') && messages.children.length === 0) {
    appendMessage('こんにちは！SalonName AIアシスタントです。営業時間・料金・予約・アクセスなど、何でもお気軽にどうぞ。', 'bot');
  }
}

// Enter キーで送信
document.getElementById('chat-input').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) handleInput();
});

// スクロールフェードイン
const observer = new IntersectionObserver(
  (entries) => entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  }),
  { threshold: 0.15 },
);
document.querySelectorAll('.fade-in').forEach((el) => observer.observe(el));

// モバイルナビの開閉
const toggle = document.getElementById('nav-toggle');
const nav = document.getElementById('main-nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => nav.classList.toggle('open'));
}
