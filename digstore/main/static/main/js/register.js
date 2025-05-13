document.addEventListener('DOMContentLoaded', function() {
    // Валидация пароля при регистрации
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const form = document.querySelector('.auth-form');

    if (form && password1 && password2) {
        form.addEventListener('submit', function(e) {
            let isValid = true;

            // Проверка совпадения паролей
            if (password1.value !== password2.value) {
                showError(password2, 'Пароли не совпадают');
                isValid = false;
            }

            // Проверка сложности пароля
            if (password1.value.length < 8) {
                showError(password1, 'Пароль должен содержать минимум 8 символов');
                isValid = false;
            }

            if (!/\d/.test(password1.value)) {
                showError(password1, 'Пароль должен содержать хотя бы одну цифру');
                isValid = false;
            }

            if (!/[a-zA-Z]/.test(password1.value)) {
                showError(password1, 'Пароль должен содержать хотя бы одну букву');
                isValid = false;
            }

            if (!isValid) {
                e.preventDefault();
            }
        });

        // Индикатор сложности пароля
        password1.addEventListener('input', function() {
            const strengthIndicator = document.createElement('div');
            strengthIndicator.className = 'password-strength';

            const strength = calculatePasswordStrength(this.value);
            strengthIndicator.innerHTML = `
                <span style="width: ${strength}%"></span>
                <p>Сложность: ${getStrengthText(strength)}</p>
            `;

            let existingIndicator = this.parentNode.querySelector('.password-strength');
            if (existingIndicator) {
                existingIndicator.replaceWith(strengthIndicator);
            } else {
                this.parentNode.appendChild(strengthIndicator);
            }
        });
    }

    function calculatePasswordStrength(password) {
        let strength = 0;

        // Длина пароля
        strength += Math.min(password.length * 5, 50);

        // Наличие цифр
        if (/\d/.test(password)) strength += 10;

        // Наличие букв в разных регистрах
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 20;

        // Специальные символы
        if (/[^a-zA-Z0-9]/.test(password)) strength += 20;

        return Math.min(strength, 100);
    }

    function getStrengthText(strength) {
        if (strength < 30) return 'Слабый';
        if (strength < 70) return 'Средний';
        return 'Сильный';
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
            if (error.textContent === message) {
                error.textContent = '';
                input.style.borderColor = '';
            }
        }, 5000);
    }
});