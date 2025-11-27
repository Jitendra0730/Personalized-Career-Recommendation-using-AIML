// Main JavaScript file for Career Compass

document.addEventListener('DOMContentLoaded', function() {

        // Email live validator
    const emailInput = document.getElementById('email');
    const emailFeedback = document.getElementById('emailFeedback');
    
    if (emailInput && emailFeedback) {
        emailInput.addEventListener('input', function () {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (this.value.length === 0) {
                emailFeedback.textContent = '';
            } else if (!emailPattern.test(this.value)) {
                emailFeedback.textContent = 'Invalid email format';
                emailFeedback.className = 'form-text text-danger';
            } else {
                emailFeedback.textContent = 'Valid email';
                emailFeedback.className = 'form-text text-success';
            }
        });
    }
    
    // Password strength checker
    const passwordInput = document.getElementById('password');
    const passwordStrength = document.getElementById('passwordStrength');
    
    if (passwordInput && passwordStrength) {
        passwordInput.addEventListener('input', function () {
            const val = this.value;
            let strength = 0;
        
            if (val.length >= 8) strength++;
            if (/[A-Z]/.test(val)) strength++;
            if (/[0-9]/.test(val)) strength++;
            if (/[^A-Za-z0-9]/.test(val)) strength++;
        
            if (val.length === 0) {
                passwordStrength.textContent = '';
            } else if (strength <= 1) {
                passwordStrength.textContent = 'Weak password';
                passwordStrength.className = 'form-text text-danger';
            } else if (strength === 2) {
                passwordStrength.textContent = 'Medium strength password';
                passwordStrength.className = 'form-text text-warning';
            } else {
                passwordStrength.textContent = 'Strong password';
                passwordStrength.className = 'form-text text-success';
            }
        });
    }
    
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });


    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    
    const salaryMinInput = document.getElementById('expected_salary_min');
    const salaryMaxInput = document.getElementById('expected_salary_max');
    
    if (salaryMinInput && salaryMaxInput) {
        function validateSalaryRange() {
            const minValue = parseInt(salaryMinInput.value) || 0;
            const maxValue = parseInt(salaryMaxInput.value) || 0;
            
            if (minValue > 0 && maxValue > 0 && minValue >= maxValue) {
                salaryMaxInput.setCustomValidity('Maximum salary must be greater than minimum salary');
            } else {
                salaryMaxInput.setCustomValidity('');
            }
        }
        
        salaryMinInput.addEventListener('input', validateSalaryRange);
        salaryMaxInput.addEventListener('input', validateSalaryRange);
    }

    
    const textAreas = document.querySelectorAll('textarea[maxlength]');
    textAreas.forEach(textArea => {
        const maxLength = textArea.getAttribute('maxlength');
        const counter = document.createElement('small');
        counter.className = 'form-text text-muted';
        counter.style.textAlign = 'right';
        counter.style.display = 'block';
        textArea.parentNode.appendChild(counter);
        
        function updateCounter() {
            const remaining = maxLength - textArea.value.length;
            counter.textContent = `${remaining} characters remaining`;
            
            if (remaining < 50) {
                counter.classList.add('text-warning');
                counter.classList.remove('text-muted');
            } else {
                counter.classList.add('text-muted');
                counter.classList.remove('text-warning');
            }
        }
        
        textArea.addEventListener('input', updateCounter);
        updateCounter(); // Initial call
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Progress bar animation
    const progressBars = document.querySelectorAll('.progress-bar');
    const animateProgressBars = () => {
        progressBars.forEach(bar => {
            const rect = bar.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            }
        });
    };

    // Animate progress bars on scroll
    window.addEventListener('scroll', animateProgressBars);
    animateProgressBars(); // Initial call

    // Form auto-save (for profile form)
    const profileForm = document.querySelector('form[action*="profile"]');
    if (profileForm) {
        let autoSaveTimeout;
        const formInputs = profileForm.querySelectorAll('input, textarea, select');
        
        formInputs.forEach(input => {
            input.addEventListener('input', function() {
                clearTimeout(autoSaveTimeout);
                autoSaveTimeout = setTimeout(() => {
                    // Show auto-save indicator
                    showAutoSaveIndicator();
                }, 2000);
            });
        });
        
        function showAutoSaveIndicator() {
            // Create or update auto-save indicator
            let indicator = document.getElementById('auto-save-indicator');
            if (!indicator) {
                indicator = document.createElement('small');
                indicator.id = 'auto-save-indicator';
                indicator.className = 'text-muted';
                indicator.style.position = 'fixed';
                indicator.style.top = '20px';
                indicator.style.right = '20px';
                indicator.style.background = 'rgba(0,0,0,0.8)';
                indicator.style.color = 'white';
                indicator.style.padding = '5px 10px';
                indicator.style.borderRadius = '5px';
                indicator.style.zIndex = '9999';
                document.body.appendChild(indicator);
            }
            
            indicator.textContent = 'Draft saved locally';
            indicator.style.display = 'block';
            
            setTimeout(() => {
                indicator.style.display = 'none';
            }, 2000);
        }
    }

    // Add loading state to buttons on form submission
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.closest('form').addEventListener('submit', function() {
            button.disabled = true;
            const originalText = button.innerHTML;
            button.innerHTML = '<span class="loading"></span> Loading...';
            
            // Re-enable button after 5 seconds as fallback
            setTimeout(() => {
                button.disabled = false;
                button.innerHTML = originalText;
            }, 5000);
        });
    });

    // Enhanced form validation messages
    const invalidInputs = document.querySelectorAll('.is-invalid');
    invalidInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.classList.remove('is-invalid');
        });
    });

    // Initialize any additional components
    initializeCustomComponents();
});

// Custom component initialization
function initializeCustomComponents() {
    // Add any custom component initialization here
    console.log('Career Compass app initialized successfully!');
}

// Utility functions
const Utils = {
    // Format currency
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Show toast notification
    showToast: function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed`;
        toast.style.top = '20px';
        toast.style.right = '20px';
        toast.style.zIndex = '9999';
        toast.style.minWidth = '300px';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }
};

// Make Utils available globally
window.Utils = Utils;
