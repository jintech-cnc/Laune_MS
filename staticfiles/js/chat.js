// La Une Multiservice — Chat Widget

const CSRF_TOKEN = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';

let chatOpened = false;
let chatInitialized = false;

function toggleChat() {
  const win = document.getElementById('chat-window');
  const iconOpen = document.getElementById('chat-icon-open');
  const iconClose = document.getElementById('chat-icon-close');
  const badge = document.getElementById('chat-badge');

  chatOpened = !chatOpened;
  win.style.display = chatOpened ? 'block' : 'none';
  iconOpen.style.display = chatOpened ? 'none' : 'block';
  iconClose.style.display = chatOpened ? 'block' : 'none';
  badge.style.display = 'none';

  if (chatOpened && !chatInitialized) {
    chatInitialized = true;
    loadHistory();
    setTimeout(() => {
      const msgs = document.getElementById('chat-messages');
      if (!msgs.children.length) {
        appendBotMessage("Bonjour ! 👋 Bienvenue chez **La Une Multiservice**.\n\nComment puis-je vous aider aujourd'hui ?\n\n• Devis gratuit\n• Nos services\n• Urgences\n• Contact", new Date().toLocaleTimeString('fr-FR', {hour:'2-digit',minute:'2-digit'}));
      }
    }, 500);
  }
  if (chatOpened) {
    setTimeout(() => document.getElementById('chat-input').focus(), 300);
  }
}

function appendMessage(sender, content, time) {
  const msgs = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = `chat-msg ${sender}`;

  // Parse markdown-like **bold** and links
  const formatted = content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" style="color:var(--gold);">$1</a>');

  div.innerHTML = `
    <div class="chat-bubble">${formatted}</div>
    <div class="chat-time">${time}</div>
  `;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function appendBotMessage(content, time) {
  // Show typing indicator first
  const msgs = document.getElementById('chat-messages');
  const typing = document.createElement('div');
  typing.className = 'chat-msg bot';
  typing.id = 'chat-typing-indicator';
  typing.innerHTML = `<div class="chat-bubble chat-typing"><span></span><span></span><span></span></div>`;
  msgs.appendChild(typing);
  msgs.scrollTop = msgs.scrollHeight;

  setTimeout(() => {
    const indicator = document.getElementById('chat-typing-indicator');
    if (indicator) indicator.remove();
    appendMessage('bot', content, time);
  }, 900);
}

function sendChat() {
  const input = document.getElementById('chat-input');
  const nameInput = document.getElementById('chat-name');
  const content = input.value.trim();
  if (!content) return;

  const now = new Date().toLocaleTimeString('fr-FR', {hour:'2-digit', minute:'2-digit'});
  appendMessage('visitor', content, now);
  input.value = '';

  fetch('/chat/send/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': CSRF_TOKEN,
    },
    body: JSON.stringify({
      message: content,
      name: nameInput ? nameInput.value.trim() : '',
    }),
  })
  .then(r => r.json())
  .then(data => {
    if (data.bot_reply) {
      appendBotMessage(data.bot_reply, data.timestamp);
    }
  })
  .catch(() => {
    appendBotMessage("Désolé, une erreur s'est produite. Veuillez réessayer ou nous appeler directement.", now);
  });
}

function loadHistory() {
  fetch('/chat/history/')
    .then(r => r.json())
    .then(data => {
      if (data.messages && data.messages.length) {
        data.messages.forEach(m => appendMessage(m.sender, m.content, m.timestamp));
      }
    })
    .catch(() => {});
}

// Show badge after 8 seconds if chat not opened
setTimeout(() => {
  if (!chatOpened) {
    const badge = document.getElementById('chat-badge');
    if (badge) badge.style.display = 'flex';
  }
}, 8000);
