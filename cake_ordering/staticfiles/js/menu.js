window.onload = function () {
        const telegramId = localStorage.getItem('telegram_id');
        
        
        if (telegramId) {
            document.getElementById('telegram_id').value = telegramId;
        }
    };
    const swup = new Swup();

document.querySelectorAll('.choose-button').forEach(button => {
    button.addEventListener('click', function (e) {
    e.preventDefault();
    const url = button.getAttribute('href');

    const overlay = document.createElement('div');
    overlay.classList.add('transition-overlay');

    const rect = button.getBoundingClientRect();
    overlay.style.left = `${rect.left + rect.width / 2}px`;
    overlay.style.top = `${rect.top + rect.height / 2}px`;

    document.body.appendChild(overlay);
    requestAnimationFrame(() => {
        overlay.classList.add('active');
    });

    setTimeout(() => {
        swup.loadPage({ url });
    }, 500);
    });
});

swup.hooks.on('contentReplaced', () => {
    const overlay = document.querySelector('.transition-overlay');
    if (overlay) overlay.remove();
});
    // Функция для инициализации Vanta.FOG
    function initVanta() {
        VANTA.FOG({
            el: "#vanta-bg",
            mouseControls: true,
            touchControls: true,
            gyroControls: false,
            minHeight: window.innerHeight,
            minWidth: window.innerWidth,
            highlightColor: 0xffd778,
            midtoneColor: 0xff8d7b,
            lowlightColor: 0xafdeff,
            baseColor: 0xbee0ff,
            blurFactor: 0.90,
            speed: 2.80,
            zoom: 0.90
        });
    }

    // Функция для обновления Vanta.FOG
    function updateVanta() {
        if (Vanta && Vanta.fog) {
            Vanta.fog.destroy();
            initVanta();
        }
    }

    // Инициализация при загрузке страницы
    document.addEventListener("DOMContentLoaded", function() {
        initVanta();

        // Обновляем Vanta.FOG при изменении размера окна
        window.addEventListener('resize', updateVanta);

        // Используем MutationObserver для отслеживания изменений в аккордеоне
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'class') {
                    const accordionItem = mutation.target;
                    if (accordionItem.classList.contains('show')) {
                        updateVanta();
                    }
                }
            });
        });

        // Наблюдаем за всеми элементами аккордеона
        const accordionItems = document.querySelectorAll('.accordion-item');
        accordionItems.forEach(function(item) {
            observer.observe(item, { attributes: true });
        });

        // Обновляем Vanta.FOG после завершения анимации аккордеона
        accordionItems.forEach(function(item) {
            const collapse = item.querySelector('.accordion-collapse');
            collapse.addEventListener('transitionend', updateVanta);
        });
    });