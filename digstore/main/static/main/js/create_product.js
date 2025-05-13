document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createProductForm');
    const imageInput = document.getElementById('id_image');
    const imagePreview = document.getElementById('imagePreview');
    const combinationsTextarea = document.getElementById('id_combinations');
    const codesCounter = document.getElementById('codesCount');

    // Превью изображения
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();

                reader.onload = function(e) {
                    imagePreview.innerHTML = `
                        <img src="${e.target.result}" alt="Превью изображения">
                        <button type="button" class="remove-image-btn">
                            <i class="bi bi-x"></i> Удалить
                        </button>
                    `;
                    imagePreview.style.display = 'block';

                    // Обработчик для кнопки удаления
                    const removeBtn = imagePreview.querySelector('.remove-image-btn');
                    removeBtn.addEventListener('click', function() {
                        imageInput.value = '';
                        imagePreview.style.display = 'none';
                        imagePreview.innerHTML = '';
                    });
                }

                reader.readAsDataURL(file);
            }
        });
    }

    // Счетчик кодов активации
    if (combinationsTextarea && codesCounter) {
        const updateCodesCount = () => {
            const codes = combinationsTextarea.value.split('\n')
                .map(code => code.trim())
                .filter(code => code.length > 0);
            codesCounter.textContent = codes.length;
        };

        combinationsTextarea.addEventListener('input', updateCodesCount);
        updateCodesCount(); // Инициализация
    }

    // Валидация формы
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;

            // Проверка количества кодов
            const codes = combinationsTextarea.value.split('\n')
                .filter(code => code.trim().length > 0);

            if (codes.length === 0) {
                alert('Добавьте хотя бы один код активации');
                isValid = false;
            }

            // Проверка изображения
            if (!imageInput.files || imageInput.files.length === 0) {
                alert('Загрузите изображение товара');
                isValid = false;
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    }
});