/**
 * CourseHub - Main JavaScript File
 * Интерактивные эффекты и улучшения UX
 */

// ===== Инициализация при загрузке страницы =====
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeScrollEffects();
    initializeFormValidation();
    initializeTooltips();
    initializeThemeToggle();
});

// ===== 1. Анимации при скролле =====
function initializeScrollEffects() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Аддение класса для анимации
                entry.target.classList.add('animate-in');
                
                // Для cards - добавляем стаггер эффект
                if (entry.target.classList.contains('course-card')) {
                    const delay = Array.from(entry.target.parentElement.children)
                        .indexOf(entry.target) * 100;
                    entry.target.style.animationDelay = delay + 'ms';
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Наблюдаем за всеми элементами которые должны анимироваться
    document.querySelectorAll('.course-card, .stats-card, .feature-box, .review-card')
        .forEach(el => observer.observe(el));
}

// ===== 2. Валидация форм с анимацией =====
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Анимация ошибок
                form.querySelectorAll('.form-control, .form-select').forEach(input => {
                    if (!input.checkValidity()) {
                        input.classList.add('shake-error');
                        setTimeout(() => input.classList.remove('shake-error'), 500);
                    }
                });
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Real-time валидация
    document.querySelectorAll('.form-control, .form-select').forEach(input => {
        input.addEventListener('blur', function() {
            if (!this.checkValidity()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });
}

// ===== 3. Инициализация анимаций элементов =====
function initializeAnimations() {
    // Navbar анимация при скролле
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop) {
                // Скролл вниз
                navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
            } else {
                // Скролл вверх
                navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.05)';
            }
            lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
        });
    }

    // Анимация для кнопок при наведении
    document.querySelectorAll('.btn-gradient, .btn-outline-gradient').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'all 0.3s ease';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// ===== 4. Tooltip инициализация (Bootstrap) =====
function initializeTooltips() {
    // Инициализация всех tooltips
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(tooltipTriggerEl => 
        new bootstrap.Tooltip(tooltipTriggerEl)
    );
}

// ===== 5. Переключатель темы =====
function initializeThemeToggle() {
    // Получаем сохраненную тему
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(newTheme);
    localStorage.setItem('theme', newTheme);
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    
    if (theme === 'dark') {
        document.body.style.backgroundColor = '#1a1a1a';
        document.body.style.color = '#fff';
    } else {
        document.body.style.backgroundColor = '#f8f9fa';
        document.body.style.color = '#333';
    }
}

// ===== 6. Smooth scroll для якорей =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });
});

// ===== 7. Поиск с live фильтрацией =====
function setupLiveSearch() {
    const searchInputs = document.querySelectorAll('input[data-live-search]');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            const targetClass = this.getAttribute('data-live-search');
            const items = document.querySelectorAll(targetClass);
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(query)) {
                    item.style.display = '';
                    item.classList.add('fade-in');
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

// ===== 8. Функции утилит =====

/**
 * Показывает notification/toast
 */
function showNotification(message, type = 'info', duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.remove();
        }
    }, duration);
}

/**
 * Копирует текст в буфер обмена
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('✓ Скопировано в буфер обмена', 'success', 2000);
    });
}

/**
 * Форматирует число как валюту
 */
function formatCurrency(amount, currency = '₸') {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: currency,
    }).format(amount).replace(currency, '').trim() + currency;
}

/**
 * Загрузчик скелета (skeleton loader)
 */
function showSkeletonLoader(container) {
    container.innerHTML = `
        <div class="skeleton">
            <div class="skeleton-line" style="height: 20px; margin-bottom: 10px;"></div>
            <div class="skeleton-line" style="height: 20px; width: 80%;"></div>
        </div>
    `;
}

// ===== 9. API помощники =====

/**
 * Отправляет AJAX запрос
 */
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, finalOptions);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showNotification('Ошибка при загрузке данных', 'danger');
        throw error;
    }
}

/**
 * Получает CSRF token
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ===== 10. Инициализация при загрузке =====
document.addEventListener('DOMContentLoaded', function() {
    setupLiveSearch();
    initializeEnrollmentButtons();
    initializeDeleteConfirmation();
});

/**
 * Обработка кнопок записи на курс
 */
function initializeEnrollmentButtons() {
    document.querySelectorAll('[data-enroll-btn]').forEach(btn => {
        btn.addEventListener('click', handleEnrollment);
    });
}

async function handleEnrollment(e) {
    e.preventDefault();
    const courseId = this.getAttribute('data-course-id');
    
    try {
        const result = await apiRequest(`/api/courses/${courseId}/enroll/`, {
            method: 'POST'
        });
        
        if (result.success) {
            showNotification('✓ Вы успешно записались на курс!', 'success');
            // Перезагружаем страницу через 1.5 сек
            setTimeout(() => location.reload(), 1500);
        }
    } catch (error) {
        showNotification('Ошибка при записи на курс', 'danger');
    }
}

/**
 * Подтверждение при удалении
 */
function initializeDeleteConfirmation() {
    document.querySelectorAll('[data-confirm-delete]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Вы уверены? Это действие нельзя отменить.')) {
                e.preventDefault();
            }
        });
    });
}

// ===== CSS Animations =====
const style = document.createElement('style');
style.textContent = `
    @keyframes shake-error {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    @keyframes fade-in {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slide-up {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .shake-error {
        animation: shake-error 0.5s;
    }

    .animate-in {
        animation: fade-in 0.6s ease-out forwards;
    }

    .fade-in {
        animation: fade-in 0.3s ease-out;
    }

    .slide-up {
        animation: slide-up 0.5s ease-out;
    }

    /* Skeleton loader styles */
    .skeleton {
        animation: skeleton-loading 1s linear infinite alternate;
    }

    .skeleton-line {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s infinite;
    }

    @keyframes skeleton-loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    /* Dark theme */
    [data-theme="dark"] {
        --primary: #3498db;
        --accent: #e67e22;
        --secondary: #34495e;
    }

    [data-theme="dark"] .navbar {
        background-color: #1a1a1a !important;
    }

    [data-theme="dark"] .course-card {
        background-color: #2a2a2a;
        color: #fff;
    }

    [data-theme="dark"] .form-control {
        background-color: #2a2a2a;
        border-color: #444;
        color: #fff;
    }

    [data-theme="dark"] .form-control:focus {
        background-color: #333;
        border-color: var(--primary);
        color: #fff;
    }
`;
document.head.appendChild(style);

console.log('✅ CourseHub JavaScript загружен успешно!');
