document.addEventListener('DOMContentLoaded', () => {
    const rxForm = document.querySelector('#rx');
    const txForm = document.querySelector('#tx');

    const messages = document.querySelector('#messages');
    const rxWaiting = document.querySelector('#rx #waiting');

    rxForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        rxWaiting.style = ''; // Show waiting text
        // Request message from server
        const numBuffers = rxForm.querySelector('input').value;
        const message = await (await fetch(`/rx/${numBuffers}`)).json();
        rxWaiting.style.display = 'none'; // Hide waiting text
        // Add message to chat log
        const newMessage = document.createElement('div');
        newMessage.className = 'message';
        const time = (new Date()).toLocaleTimeString([], {hour12: false});
        newMessage.textContent = time + ': ' + message;
        messages.appendChild(newMessage);
    });

    txForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        // Send message to server
        const message = txForm.querySelector('input').value;
        fetch('/tx', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(message)
        });
        // Add message to chat log
        const newMessage = document.createElement('div');
        newMessage.className = 'message';
        newMessage.classList.add('tx-message');
        const time = (new Date()).toLocaleTimeString([], {hour12: false});
        newMessage.textContent = time + ': ' + message;
        messages.appendChild(newMessage);
        txForm.reset();
    });
});
