const loginTab = document.getElementById('login-tab');
const registerTab = document.getElementById('register-tab');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

function switchTab(activeTab, activeForm, inactiveTab, inactiveForm) {
    activeTab.classList.add('active');
    inactiveTab.classList.remove('active');
    activeForm.classList.add('active');
    inactiveForm.classList.remove('active');
}

loginTab.addEventListener('click', () => switchTab(loginTab, loginForm, registerTab, registerForm));
registerTab.addEventListener('click', () => switchTab(registerTab, registerForm, loginTab, loginForm));

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = loginForm.querySelector('input[type="text"]').value;
    const password = loginForm.querySelector('input[type="password"]').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ login: username, password: password }),
        })
        if (response.ok) {
            const data = await response.json();
            window.location.href = 'http://127.0.0.1:8000/chat';
        } else {
            alert('Ошибка входа. Проверьте логин и пароль.');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при попытке входа.');
    }
});

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = registerForm.querySelector('input[type="text"]').value;
    const password = registerForm.querySelector('input[type="password"]').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/auth/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ login: username, password: password }),
        });
        if (response.ok) {
            alert('Регистрация успешна. Теперь вы можете войти.');
            switchTab(loginTab, loginForm, registerTab, registerForm);
        } else {
            alert('Ошибка регистрации. Возможно, этот логин уже занят.');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при попытке регистрации.');
    }
});