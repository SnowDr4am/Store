document.addEventListener('DOMContentLoaded', function() {
    // Плавная прокрутка к секциям
    const scrollArrow = document.querySelector('.scrolling-arrow');
    if (scrollArrow) {
        scrollArrow.addEventListener('click', function() {
            const missionSection = document.querySelector('.mission-section');
            missionSection.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Переключение вкладок
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Удаляем активный класс у всех кнопок
            tabButtons.forEach(btn => btn.classList.remove('active'));

            // Добавляем активный класс текущей кнопке
            this.classList.add('active');

            // Скрываем все вкладки
            const tabContents = document.querySelectorAll('.tab-content');
            tabContents.forEach(content => content.classList.remove('active'));

            // Показываем нужную вкладку
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Анимация при скролле
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.mission-card, .team-card, .feature-image img');

        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;

            if (elementPosition < screenPosition) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Инициализация анимации
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Запускаем при загрузке

    // Инициализация состояния элементов
    const missionCards = document.querySelectorAll('.mission-card');
    const teamCards = document.querySelectorAll('.team-card');
    const featureImages = document.querySelectorAll('.feature-image img');

    missionCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });

    teamCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        card.style.transition = 'opacity 0.6s ease 0.2s, transform 0.6s ease 0.2s';
    });

    featureImages.forEach(img => {
        img.style.opacity = '0';
        img.style.transition = 'opacity 1s ease 0.4s';
    });
});