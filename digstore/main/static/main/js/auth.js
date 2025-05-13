document.addEventListener('DOMContentLoaded', function() {
    // Переключение видимости пароля
    const togglePassword = document.querySelector('.toggle-password');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const passwordInput = document.getElementById('password');
            const icon = this.querySelector('i');

            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    }

    // Валидация формы
    const authForm = document.querySelector('.auth-form');
    if (authForm) {
        authForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username');
            const password = document.getElementById('password');
            let isValid = true;

            // Простая валидация
            if (username.value.trim() === '') {
                showError(username, 'Введите имя пользователя');
                isValid = false;
            }

            if (password.value.trim() === '') {
                showError(password, 'Введите пароль');
                isValid = false;
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    }

    function showError(input, message) {
        const formGroup = input.closest('.form-group');
        let error = formGroup.querySelector('.error-message');

        if (!error) {
            error = document.createElement('div');
            error.className = 'error-message';
            formGroup.appendChild(error);
        }

        error.textContent = message;
        input.style.borderColor = '#ff4d4d';

        setTimeout(() => {
            error.textContent = '';
            input.style.borderColor = '';
        }, 3000);
    }
});