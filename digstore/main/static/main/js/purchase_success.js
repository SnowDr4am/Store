document.addEventListener('DOMContentLoaded', function() {
    // Копирование кода
    const copyBtn = document.querySelector('.copy-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const code = document.querySelector('.code-value').textContent;
            navigator.clipboard.writeText(code).then(() => {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check"></i> Скопировано!';
                this.classList.add('copied');

                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('copied');
                }, 2000);
            });
        });
    }
});