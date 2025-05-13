document.addEventListener('DOMContentLoaded', function() {
    // Инициализация копирования кода
    const copyBtn = document.querySelector('.copy-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const code = this.getAttribute('data-clipboard-text');
            navigator.clipboard.writeText(code).then(() => {
                // Временное изменение стиля кнопки
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check"></i> Скопировано!';
                this.style.backgroundColor = '#00ccff';
                this.style.color = '#121212';

                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.backgroundColor = '';
                    this.style.color = '';
                }, 2000);
            }).catch(err => {
                console.error('Ошибка копирования: ', err);
            });
        });
    }

    // Инициализация звездного рейтинга
    const stars = document.querySelectorAll('.stars-rating label');
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const ratingValue = this.previousElementSibling.value;
            console.log('Выбрана оценка: ', ratingValue);
        });
    });
});