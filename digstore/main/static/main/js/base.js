document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.product-header');
    const fixedHeader = document.querySelector('.fixed-header');
    const navbar = document.querySelector('.navbar');

    if (header && fixedHeader && navbar) {
        window.addEventListener('scroll', function() {
            const headerRect = header.getBoundingClientRect();
            if (headerRect.top < 0) {
                fixedHeader.classList.add('show');
                navbar.style.display = 'none';
            } else {
                fixedHeader.classList.remove('show');
                navbar.style.display = 'block';
            }
        });
    }

    const priceRange = document.getElementById('price-range');
    const ratingRange = document.getElementById('rating-range');

    if (priceRange) {
        priceRange.addEventListener('input', function() {
            document.getElementById('price-value').textContent = this.value + ' ₽';
        });
    }

    if (ratingRange) {
        ratingRange.addEventListener('input', function() {
            document.getElementById('rating-value').textContent = this.value;
        });
    }
});