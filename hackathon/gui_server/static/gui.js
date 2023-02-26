document.addEventListener('DOMContentLoaded', () => {
    rxForm = document.querySelector('#rx');
    txForm = document.querySelector('#tx');

    rxText = document.querySelector('#rx #text');
    rxWaiting = document.querySelector('#rx #waiting');

    rxForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        numBuffers = rxForm.querySelector('input').value;
        rxWaiting.style = ''; // Hide waiting text
        message = await (await fetch(`/rx/${numBuffers}`)).json();
        rxWaiting.style.display = 'none'; // Show waiting text
        rxText.textContent = message;
        rxForm.reset();
    });

    txForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        message = txForm.querySelector('input').value;
        fetch('/tx', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(message)
        });
        txForm.reset();
    });
});
