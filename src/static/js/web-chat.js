const userName = sessionStorage.getItem('userName');

async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function main(login) {
    const url = `http://127.0.0.1:8000/user/id/${login}`;
    const id = await fetchData(url);
    getMessages()
    .then(messages => {
        displayMessages(messages);
    })
    .catch(error => {
        console.error('Failed to get messages:', error);
    });
    connectWebSocket(id["id"]);
}

document.addEventListener("DOMContentLoaded", () => {
    if (userName) {
        document.getElementById('username').innerText = userName;
    }
});


function showMessage(message) {
    const messageContainer = document.getElementById('messageContainer');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageContainer.appendChild(messageElement);
}

function connectWebSocket(id) {
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/' + id);
    console.log('ws://127.0.0.1:8000/ws/' + id)

    socket.addEventListener('open', (event) => {
        showMessage('Подключен к серверу.');
    });

    socket.onmessage = (event) => {
        showMessage(event.data)
    }

    socket.addEventListener('close', (event) => {
        showMessage('Соединение закрыто.');
    });

    const inputText = document.getElementById("messageInput");
    const submitButton = document.getElementById("submitButton");

    submitButton.addEventListener("click", function () {
        const inputValue = inputText.value;
        socket.send(inputValue)
        inputText.value = '';
    });

    inputText.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const inputValue = inputText.value;
            socket.send(inputValue)
            inputText.value = '';
        }
    });
}

async function getLoginById(user_id) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/user/login/${user_id}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const login = await response.json();
        return login;
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function getMessages() {
    try {
        const response = await fetch('http://127.0.0.1:8000/chat/read-all-messages');
        const messages = await response.json();
        return messages;
    } catch (error) {
        console.error('Error fetching messages:', error);
        throw error;
    }
}

function displayMessages(messages) {
    const chatBox = document.getElementById('messageContainer');
    messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = `${message.sender_id}: ${message.message}`;
        chatBox.appendChild(messageDiv);
    });
}



main(userName).catch(error => {
    console.error('Ошибка в main:', error);
});
