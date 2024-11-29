const userName = localStorage.getItem('userName');

async function getIdByLogin(url) {
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
    const id = await getIdByLogin(url);
    connectWebSocket(id["id"]);
}

document.addEventListener("DOMContentLoaded", () => {
    if (userName) {
        document.getElementById('username').innerText = userName;
    }
});

function showMessage(sender, content, isSent) {
    const container = document.getElementById('messageContainer');
    const wrapper = document.createElement('div');
    wrapper.className = 'message-wrapper';

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isSent ? 'sent' : 'received'}`;
    messageDiv.textContent = content;

    const senderDiv = document.createElement('div');
    senderDiv.className = 'message-sender';
    senderDiv.textContent = sender;

    wrapper.appendChild(messageDiv);
    wrapper.appendChild(senderDiv);
    container.appendChild(wrapper);

    container.scrollTop = container.scrollHeight;
}

function connectWebSocket(id) {
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/' + id);
    console.log('ws://127.0.0.1:8000/ws/' + id)

    socket.onopen = function() {
        alert("Соединение установлено");
    };

    socket.onerror = function(error) {
        alert("Ошибка " + error.message);
    };

    socket.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            const sender = data["sender"];
            const content = data["content"];
            if (sender != userName) {
                showMessage(sender, content, false);
            } else {
                showMessage(sender, content, true);
            }
        } catch (e) {
            console.error('Error parsing message:', e);
        }
    };

    socket.onclose = function() {
        alert("Соединение закрыто");
    };

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

main(userName).catch(error => {
    console.error('Ошибка в main:', error);
});
