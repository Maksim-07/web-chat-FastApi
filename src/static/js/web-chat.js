const token = localStorage.getItem('token');

var login;

async function getUser(url) {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token,
            },
        })
        if (!response.ok) {
            window.location.href = "http://127.0.0.1:8000/auth";
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function main(token) {
    const url = `http://127.0.0.1:8000/api/users/me`;
    const data = await getUser(url);

    const user_id = data.id;
    globalThis.login = data.login;

    document.getElementById('username').innerText = login;

    connectWebSocket(user_id);
}

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
    const socket = new WebSocket(`ws://127.0.0.1:8000/api/ws/${id}?token=${token}`);

    socket.onopen = function() {
        alert("Соединение установлено");
    };

    socket.onerror = function(error) {
        alert("Ошибка " + error.message);
    };

    socket.onmessage = function(event) {
        try {
            const d = JSON.parse(event.data);
            const data = JSON.parse(d);
            const sender = data["login"];
            const content = data["message"];
            if (sender != login) {
                showMessage(sender, content, false);
            } else {
                showMessage(sender, content, true);
            }
        } catch (e) {
            console.error('Error parsing message:', e);
        }
    };

    socket.onclose = function() {
        if (event.code == 1006) {
            window.location.href = "/auth";
        }
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

main(token).catch(error => {
    console.error('Ошибка в main:', error);
});
