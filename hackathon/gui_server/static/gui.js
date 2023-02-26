document.addEventListener('DOMContentLoaded', () => {
    const rxForm = document.querySelector('#rx');
    const txForm = document.querySelector('#tx');

    const rxMessages = document.querySelector('#rx #messages');
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
        rxMessages.appendChild(newMessage);
        rxForm.reset();
    });

    txForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const message = txForm.querySelector('input').value;
        fetch('/tx', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(message)
        });
        txForm.reset();
    });
});
