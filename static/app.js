const form = document.querySelector('#chat-form');
const input = document.querySelector('#message-input');
const messages = document.querySelector('#messages');
const welcome = document.querySelector('#welcome');
const counter = document.querySelector('#counter');
const sendButton = document.querySelector('.send-button');
const newChat = document.querySelector('#new-chat');

function addMessage(text, role) {
  const message = document.createElement('div');
  message.className = `message ${role}`;

  if (role === 'assistant') {
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = 'O';
    message.appendChild(avatar);
  }

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  bubble.textContent = text;
  message.appendChild(bubble);
  messages.appendChild(message);
  messages.scrollTop = messages.scrollHeight;
}

function setTyping(isTyping) {
  const existing = document.querySelector('#typing');
  if (isTyping && !existing) {
    const indicator = document.createElement('div');
    indicator.id = 'typing';
    indicator.className = 'message typing';
    indicator.textContent = 'Orbit is thinking...';
    messages.appendChild(indicator);
    messages.scrollTop = messages.scrollHeight;
  } else if (!isTyping && existing) {
    existing.remove();
  }
}

function resizeInput() {
  input.style.height = 'auto';
  input.style.height = `${Math.min(input.scrollHeight, 150)}px`;
  counter.textContent = `${input.value.length} / 2000`;
}

async function sendMessage(text) {
  const message = text.trim();
  if (!message || sendButton.disabled) return;

  welcome?.remove();
  addMessage(message, 'user');
  input.value = '';
  resizeInput();
  sendButton.disabled = true;
  setTyping(true);

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'The assistant could not respond.');
    addMessage(data.bot, 'assistant');
  } catch (error) {
    addMessage(`Sorry, ${error.message}`, 'assistant');
  } finally {
    setTyping(false);
    sendButton.disabled = false;
    input.focus();
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

input.addEventListener('input', resizeInput);
input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

document.querySelectorAll('[data-prompt]').forEach((button) => {
  button.addEventListener('click', () => sendMessage(button.dataset.prompt));
});

newChat.addEventListener('click', () => {
  messages.innerHTML = '';
  window.location.reload();
});
