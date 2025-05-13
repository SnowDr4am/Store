document.addEventListener('DOMContentLoaded', function() {
    const productHeader = document.querySelector('.product-header');
    const fixedHeader = document.querySelector('.fixed-product-header');

    if (productHeader && fixedHeader) {
        window.addEventListener('scroll', function() {
            const headerRect = productHeader.getBoundingClientRect();
            if (headerRect.top < 0) {
                fixedHeader.classList.add('show');
            } else {
                fixedHeader.classList.remove('show');
            }
        });

        // Устанавливаем изображение для фиксированного хедера
        const mainImage = document.querySelector('.product-main-image');
        const fixedImage = document.querySelector('.fixed-product-image');
        if (mainImage && fixedImage) {
            fixedImage.style.backgroundImage = `url(${mainImage.src})`;
        }
    }
});