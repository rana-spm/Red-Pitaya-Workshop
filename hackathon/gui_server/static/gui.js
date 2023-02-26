document.addEventListener('DOMContentLoaded', () => {
  const messages = document.querySelector('main');
  const form = document.querySelector('form');
  const input = document.querySelector('input');

  const numBuffers = 100;
  async function rx() {
    return await (await fetch(`/rx/${numBuffers}`)).json();
  }

  async function getMessage() {
    // Request message from server
    const message = await rx();
    // Add message to chat log
    addMessage(message);
  }

  async function tx(message) {
    // Transmit message to server
    await (await fetch('/tx', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(message)
    })).json();
    // Request message from server
    getMessage();
  }

  function addMessage(message, self = false) {
    const newMessage = document.createElement('div');
    if (self) newMessage.className = 'self-message';
    const time = (new Date()).toLocaleTimeString([], {hour12: false});
    newMessage.textContent = `[${time}] ${message}`;
    messages.appendChild(newMessage);
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    // Get message from text input
    const message = input.value;
    if (message) {
      // Transmit message to server
      await tx(message);
      // Add message to chat log
      addMessage(message, true);
      // Clear text input
      form.reset();
    }
  });
});
