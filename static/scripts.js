document.addEventListener('DOMContentLoaded', function() {
    // Пример простой анимации с использованием JavaScript
    const elements = document.querySelectorAll('.feature-card');
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = 1;
            el.style.transform = 'translateY(0)';
        }, index * 200);
    });
});