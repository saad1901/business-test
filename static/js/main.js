// Custom Resin Art Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Image preview for file inputs
    const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Create or update preview
                    let preview = input.parentNode.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.className = 'image-preview mt-2';
                        input.parentNode.appendChild(preview);
                    }
                    preview.innerHTML = `
                        <img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px; max-height: 200px;">
                        <button type="button" class="btn btn-sm btn-outline-danger ms-2" onclick="clearImagePreview(this)">
                            <i class="bi bi-x"></i> Remove
                        </button>
                    `;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Price calculation for quantity changes
    const quantityInputs = document.querySelectorAll('input[type="number"][id*="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('input', function() {
            calculatePrice(this);
        });
    });

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Mobile menu enhancement
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking on a link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Show success feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check"></i> Copied!';
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            });
        });
    });
});

// Global functions
function clearImagePreview(button) {
    const preview = button.parentNode;
    const fileInput = preview.parentNode.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.value = '';
    }
    preview.remove();
}

function calculatePrice(quantityInput) {
    const quantity = parseInt(quantityInput.value) || 1;
    const unitPriceElement = document.getElementById('unit-price');
    const totalPriceElement = document.getElementById('total-price');
    const quantityDisplayElement = document.getElementById('quantity-display');
    
    if (unitPriceElement && totalPriceElement) {
        const unitPrice = parseFloat(unitPriceElement.textContent);
        const totalPrice = unitPrice * quantity;
        
        totalPriceElement.textContent = `₹${totalPrice.toFixed(2)}`;
        if (quantityDisplayElement) {
            quantityDisplayElement.textContent = quantity;
        }
    }
}

// AJAX helper function
function makeAjaxRequest(url, data, method = 'POST') {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .catch(error => {
        console.error('AJAX Error:', error);
        throw error;
    });
}

// Show loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center';
    overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
    overlay.style.zIndex = '9999';
    overlay.innerHTML = `
        <div class="text-center text-white">
            <div class="spinner-border mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div>Processing...</div>
        </div>
    `;
    document.body.appendChild(overlay);
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

// Validate file upload
function validateFileUpload(input, maxSize = 5 * 1024 * 1024, allowedTypes = ['image/jpeg', 'image/png', 'image/gif']) {
    const file = input.files[0];
    if (!file) return true;
    
    if (file.size > maxSize) {
        alert(`File size should be less than ${maxSize / (1024 * 1024)}MB`);
        input.value = '';
        return false;
    }
    
    if (!allowedTypes.includes(file.type)) {
        alert('Please upload a valid image file (JPEG, PNG, or GIF)');
        input.value = '';
        return false;
    }
    
    return true;
}

// Debounce function for search/input optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}