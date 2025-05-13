document.addEventListener('DOMContentLoaded', function() {
    const carousels = document.querySelectorAll('.products-carousel');

    carousels.forEach(carousel => {
        const prevBtn = carousel.querySelector('.carousel-prev');
        const nextBtn = carousel.querySelector('.carousel-next');
        const productsGrid = carousel.querySelector('.products-grid');
        const productCard = carousel.querySelector('.product-card');

        if (!productsGrid || !productCard) return;

        const cardWidth = productCard.offsetWidth + 20; // + gap

        prevBtn.addEventListener('click', () => {
            productsGrid.scrollBy({
                left: -cardWidth,
                behavior: 'smooth'
            });
        });

        nextBtn.addEventListener('click', () => {
            productsGrid.scrollBy({
                left: cardWidth,
                behavior: 'smooth'
            });
        });
    });
});

function scrollCarousel(track, scrollAmount) {
    const currentScroll = track.scrollLeft;
    const maxScroll = track.scrollWidth - track.clientWidth;

    let newScroll = currentScroll + scrollAmount;
    newScroll = Math.max(0, Math.min(newScroll, maxScroll));

    track.scrollTo({
        left: newScroll,
        behavior: 'smooth'
    });
}