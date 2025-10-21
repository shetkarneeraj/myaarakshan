// Main JavaScript for Maratha Arakshan Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            // Only process if href is not just '#' and has a valid target
            if (href && href !== '#' && href.length > 1) {
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Auto-hide alerts after 5 seconds (DISABLED for important notes)
    // setTimeout(function() {
    //     const alerts = document.querySelectorAll('.alert');
    //     alerts.forEach(alert => {
    //         const bsAlert = new bootstrap.Alert(alert);
    //         bsAlert.close();
    //     });
    // }, 5000);

    // Search form enhancements
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        const searchInputs = searchForm.querySelectorAll('input[type="text"], input[type="search"]');
        
        searchInputs.forEach(input => {
            input.addEventListener('input', function() {
                // Add loading state when typing
                if (this.value.length > 2) {
                    this.classList.add('border-primary');
                } else {
                    this.classList.remove('border-primary');
                }
            });
        });
    }

    // Mobile menu improvements
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navbarToggler.contains(e.target) && 
                !navbarCollapse.contains(e.target) && 
                navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });

        // Close mobile menu when clicking on nav links (but not dropdown toggles)
        const navLinks = navbarCollapse.querySelectorAll('.nav-link:not(.dropdown-toggle)');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }

    // Mobile dropdown functionality
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const dropdown = this.closest('.dropdown');
            const menu = dropdown.querySelector('.dropdown-menu');
            
            // Close other dropdowns
            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                if (openMenu !== menu) {
                    openMenu.classList.remove('show');
                    openMenu.previousElementSibling.setAttribute('aria-expanded', 'false');
                }
            });
            
            // Toggle current dropdown
            if (menu.classList.contains('show')) {
                menu.classList.remove('show');
                this.setAttribute('aria-expanded', 'false');
            } else {
                menu.classList.add('show');
                this.setAttribute('aria-expanded', 'true');
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
                menu.previousElementSibling.setAttribute('aria-expanded', 'false');
            });
        }
    });

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' 
                    });
                }
            }
            form.classList.add('was-validated');
        });
    });

    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remove all non-digits
            let value = this.value.replace(/\D/g, '');
            
            // Limit to 10 digits
            if (value.length > 10) {
                value = value.slice(0, 10);
            }
            
            this.value = value;
            
            // Validation feedback
            if (value.length === 10) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else if (value.length > 0) {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-valid', 'is-invalid');
            }
        });
    });

    // Reservation number formatting
    const reservationInputs = document.querySelectorAll('input[name="reservation_number"]');
    reservationInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Convert to uppercase
            this.value = this.value.toUpperCase();
            
            // Basic validation pattern (can be customized)
            const pattern = /^[A-Z]{1,3}\/\d{4}\/\d{1,6}$/;
            if (pattern.test(this.value)) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else if (this.value.length > 0) {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-valid', 'is-invalid');
            }
        });
    });

    // Card hover effects
    const hoverCards = document.querySelectorAll('.hover-card');
    hoverCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Loading states for buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                // Add loading state
                const originalText = this.innerHTML;
                this.innerHTML = '<span class="loading me-2"></span>सबमिट हो रहा है...';
                this.disabled = true;
                
                // Reset after 3 seconds (form should redirect before this)
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }, 3000);
            }
        });
    });

    // Back to top button
    const backToTopButton = createBackToTopButton();
    
    function createBackToTopButton() {
        const button = document.createElement('button');
        button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        button.className = 'btn btn-primary position-fixed';
        button.style.cssText = `
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            z-index: 1000;
            display: none;
            opacity: 0;
            transition: all 0.3s ease;
        `;
        
        button.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        document.body.appendChild(button);
        
        // Show/hide based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                button.style.display = 'block';
                setTimeout(() => button.style.opacity = '1', 10);
            } else {
                button.style.opacity = '0';
                setTimeout(() => button.style.display = 'none', 300);
            }
        });
        
        return button;
    }

    // Dynamic statistics counter (if on homepage)
    const statisticElements = document.querySelectorAll('.card-body h3');
    if (statisticElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        });

        statisticElements.forEach(el => {
            observer.observe(el);
        });
    }

    function animateCounter(element) {
        const finalValue = parseInt(element.textContent.replace(/\D/g, ''));
        if (finalValue > 0) {
            let currentValue = 0;
            const increment = Math.ceil(finalValue / 30);
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= finalValue) {
                    currentValue = finalValue;
                    clearInterval(timer);
                }
                element.textContent = currentValue + (element.textContent.includes('+') ? '+' : '');
            }, 50);
        }
    }

    // Search suggestions (can be enhanced with API)
    const searchInputs = document.querySelectorAll('input[name="q"], input[name="village"], input[name="surname"]');
    searchInputs.forEach(input => {
        input.addEventListener('focus', function() {
            // You can add search suggestions here
            this.style.borderColor = '#ff6b35';
        });
        
        input.addEventListener('blur', function() {
            this.style.borderColor = '';
        });
    });

    // Print functionality
    if (window.location.pathname.includes('/village/')) {
        addPrintButton();
    }

    function addPrintButton() {
        const printButton = document.createElement('button');
        printButton.innerHTML = '<i class="fas fa-print me-2"></i>प्रिंट करा';
        printButton.className = 'btn btn-outline-secondary btn-sm';
        printButton.addEventListener('click', () => window.print());
        
        const cardHeader = document.querySelector('.card-header');
        if (cardHeader) {
            cardHeader.appendChild(printButton);
        }
    }
});

// Utility functions
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed`;
    toast.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(toast);
    setTimeout(() => toast.style.opacity = '1', 10);
    setTimeout(() => toast.remove(), 5000);
}

function formatPhoneNumber(phone) {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 10) {
        return `${cleaned.slice(0, 5)} ${cleaned.slice(5)}`;
    }
    return phone;
}

// Service Worker for offline support (progressive web app)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed:', err);
            });
    });
}
