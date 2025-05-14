document.addEventListener('DOMContentLoaded', function() {
    // Показ/скрытие фиксированного хедера
    const productHeader = document.querySelector('.product-header');
    const fixedHeader = document.querySelector('.fixed-product-header');

    if (productHeader && fixedHeader) {
        window.addEventListener('scroll', function() {
            const headerRect = productHeader.getBoundingClientRect();
            if (headerRect.top < 0) {
                fixedHeader.style.display = 'block';
            } else {
                fixedHeader.style.display = 'none';
            }
        });
    }
});