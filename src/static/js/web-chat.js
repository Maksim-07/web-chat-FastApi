function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

const id = getRandomInt(1, 1000);

const userName = sessionStorage.getItem('userName');

document.addEventListener("DOMContentLoaded", () => {
    if (userName) {
        document.getElementById('username').innerText = userName;
    }
});

const socket = new WebSocket('ws://127.0.0.1:8000/ws/'+id);
console.log('ws://127.0.0.1:8000/ws/'+id)

function showMessage(message) {
    const messageContainer = document.getElementById('messageContainer');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageContainer.appendChild(messageElement);
}

socket.addEventListener('open', (event) => {
    showMessage('Connected to server.');
});

socket.onmessage = (event) => {
    showMessage(event.data)
}

socket.addEventListener('close', (event) => {
    showMessage('Connection closed.');
});

const inputText = document.getElementById("messageInput");
const submitButton = document.getElementById("submitButton");

submitButton.addEventListener("click", function () {
    const inputValue = inputText.value;
    socket.send(inputValue)
});