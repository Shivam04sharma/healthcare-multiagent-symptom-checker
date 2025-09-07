// HEalthcare 

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
   
    initializeFormHandling();
    initializeUIEnhancements();
    initializeAccessibility();
    console.log('HealthCheck AI initialized successfully');
}

function initializeFormHandling() {
    const symptomForm = document.getElementById('symptom-form');
    const submitBtn = document.getElementById('submit-btn');
    
    if (symptomForm && submitBtn) {
        symptomForm.addEventListener('submit', function(e) {
            handleFormSubmission(e, submitBtn);
        });
        
        const symptomsTextarea = document.getElementById('symptoms');
        if (symptomsTextarea) {
            symptomsTextarea.addEventListener('input', function() {
                validateSymptoms(this, submitBtn);
            });
        }
        const ageInput = document.getElementById('age');
        if (ageInput) {
            ageInput.addEventListener('input', function() {
                validateAge(this);
            });
        }
    }
}

function handleFormSubmission(event, submitBtn) {
    showLoadingState(submitBtn);
    
    const symptomsTextarea = document.getElementById('symptoms');
    const ageInput = document.getElementById('age');
    
    if (!validateSymptoms(symptomsTextarea, submitBtn)) {
        hideLoadingState(submitBtn);
        event.preventDefault();
        return false;
    }
    
    if (ageInput && ageInput.value && !validateAge(ageInput)) {
        hideLoadingState(submitBtn);
        event.preventDefault();
        return false;
    }

    console.log('Form submitted successfully');
    setTimeout(() => {
        hideLoadingState(submitBtn);
    }, 30000); 
}

function validateSymptoms(textarea, submitBtn) {
    const symptoms = textarea.value.trim();
    const minLength = 10;
    
    removeErrorMessage(textarea);
    
    if (symptoms.length < minLength) {
        showErrorMessage(textarea, `Please provide more detailed symptoms (at least ${minLength} characters)`);
        if (submitBtn) {
            submitBtn.disabled = true;
        }
        return false;
    }
    
    // Check potentially dangerous input
    const dangerousPatterns = [
        /<script/i,
        /javascript:/i,
        /on\w+\s*=/i
    ];
    
    for (let pattern of dangerousPatterns) {
        if (pattern.test(symptoms)) {
            showErrorMessage(textarea, 'Please enter only symptom descriptions without special char');
            if (submitBtn) {
                submitBtn.disabled = true;
            }
            return false;
        }
    }

    if (submitBtn) {
        submitBtn.disabled = false;
    }
    return true;
}

function validateAge(ageInput) {
    const age = parseInt(ageInput.value);

    removeErrorMessage(ageInput);
    
    if (ageInput.value && (isNaN(age) || age < 0 || age > 150)) {
        showErrorMessage(ageInput, 'Please enter a valid age between 0 and 150');
        return false;
    }
    
    return true;
}

function showErrorMessage(input, message) {
    
    removeErrorMessage(input);

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
        color: #e74c3c;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        padding: 0.5rem;
        background: #fdf2f2;
        border: 1px solid #fecaca;
        border-radius: 4px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    `;
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;

    input.parentNode.insertBefore(errorDiv, input.nextSibling);

    input.style.borderColor = '#e74c3c';
    input.style.boxShadow = '0 0 0 3px rgba(231, 76, 60, 0.1)';
}

function removeErrorMessage(input) {
    const errorMessage = input.parentNode.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }

    input.style.borderColor = '';
    input.style.boxShadow = '';
}

function showLoadingState(submitBtn) {
    if (!submitBtn) return;
    
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    
    const spinner = submitBtn.querySelector('.loading-spinner');
    const text = submitBtn.querySelector('span');
    
    if (spinner) spinner.style.display = 'inline-block';
    if (text) text.style.display = 'none';
}

function hideLoadingState(submitBtn) {
    if (!submitBtn) return;
    
    submitBtn.classList.remove('loading');
    submitBtn.disabled = false;
    
    const spinner = submitBtn.querySelector('.loading-spinner');
    const text = submitBtn.querySelector('span');
    
    if (spinner) spinner.style.display = 'none';
    if (text) text.style.display = 'inline';
}

function initializeUIEnhancements() {
    
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
    
  
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            autoResizeTextarea(this);
        });
        
    
        autoResizeTextarea(textarea);
    });
    
 
    const cards = document.querySelectorAll('.condition-item, .feature-item');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    initializeMedicineTooltips();
    
    initializeCopyFunctionality();
}

function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.max(textarea.scrollHeight, 120) + 'px';
}

function initializeMedicineTooltips() {
    const medicineTags = document.querySelectorAll('.medicine-tag');
    
    medicineTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            showMedicineTooltip(this);
        });
        
        tag.addEventListener('mouseleave', function() {
            hideMedicineTooltip(this);
        });
    });
}

function showMedicineTooltip(element) {
    const medicine = element.textContent.trim();
    const tooltipText = getMedicineInfo(medicine);
    
    if (!tooltipText) return;
    
    const tooltip = document.createElement('div');
    tooltip.className = 'medicine-tooltip';
    tooltip.style.cssText = `
        position: absolute;
        background: #2c3e50;
        color: white;
        padding: 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        max-width: 200px;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        pointer-events: none;
    `;
    tooltip.textContent = tooltipText;
    
    document.body.appendChild(tooltip);
  
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + 'px';
    tooltip.style.top = (rect.bottom + 5) + 'px';
    
    element._tooltip = tooltip;
}

function hideMedicineTooltip(element) {
    if (element._tooltip) {
        element._tooltip.remove();
        delete element._tooltip;
    }
}

function getMedicineInfo(medicine) {
    const medicineInfo = {
        'Acetaminophen': 'Pain reliever and fever reducer. Follow dosage instructions.',
        'Ibuprofen': 'Anti-inflammatory pain reliever. Take with food.',
        'Aspirin': 'Pain reliever with blood-thinning properties.',
        'Antihistamines': 'Help with allergic reactions and itching.',
        'Decongestants': 'Reduce nasal congestion and stuffiness.',
        'Cough suppressants': 'Help reduce coughing symptoms.',
        'Probiotics': 'Support digestive health and gut bacteria.'
    };
    
    return medicineInfo[medicine] || null;
}

function initializeCopyFunctionality() {
   
    if (window.location.pathname.includes('result') && !window.matchMedia('print').matches) {
        addCopyButton();
    }
}

function addCopyButton() {
    const actionButtons = document.querySelector('.action-buttons');
    if (!actionButtons) return;
    
    const copyBtn = document.createElement('button');
    copyBtn.className = 'btn btn-secondary';
    copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy Results';
    copyBtn.addEventListener('click', copyResultsToClipboard);
    
    actionButtons.appendChild(copyBtn);
}

function copyResultsToClipboard() {
    const resultsContainer = document.querySelector('.results-container');
    if (!resultsContainer) return;
    
    
    let resultsText = 'HealthCheck AI - Symptom Analysis Results\n';
    resultsText += '=' .repeat(50) + '\n\n';
    
    
    const symptoms = document.querySelector('.user-input');
    if (symptoms) {
        resultsText += 'Symptoms: ' + symptoms.textContent.trim() + '\n\n';
    }
    
  
    const conditions = document.querySelectorAll('.condition-name');
    if (conditions.length > 0) {
        resultsText += 'Potential Conditions:\n';
        conditions.forEach((condition, index) => {
            resultsText += `${index + 1}. ${condition.textContent.trim()}\n`;
        });
        resultsText += '\n';
    }
    

    resultsText += 'DISCLAIMER: This is for educational purposes only. Consult a healthcare professional for medical advice.\n';
    
  
    navigator.clipboard.writeText(resultsText).then(() => {
        showNotification('Results copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy results', 'error');
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    const colors = {
        success: '#27ae60',
        error: '#e74c3c',
        info: '#3498db',
        warning: '#f39c12'
    };
    
    notification.style.background = colors[type] || colors.info;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
   
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

function initializeAccessibility() {
    
    const interactiveElements = document.querySelectorAll('.condition-item, .feature-item, .btn');
    
    interactiveElements.forEach(element => {
        if (!element.hasAttribute('tabindex')) {
            element.setAttribute('tabindex', '0');
        }
        
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.setAttribute('aria-describedby', 'submit-help');
        
        const helpText = document.createElement('div');
        helpText.id = 'submit-help';
        helpText.className = 'sr-only';
        helpText.textContent = 'Submit your symptoms for AI analysis';
        submitBtn.parentNode.appendChild(helpText);
    }
    
    
    const formInputs = document.querySelectorAll('input, textarea');
    formInputs.forEach(input => {
        const label = document.querySelector(`label[for="${input.id}"]`);
        if (label && !input.hasAttribute('aria-labelledby')) {
            input.setAttribute('aria-labelledby', input.id + '-label');
            label.id = input.id + '-label';
        }
    });
}

async function checkSystemStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.success) {
            console.log('System status:', data.status);
            console.log('Groq API available:', data.groq_api_available);
            return data;
        } else {
            console.error('System status check failed:', data.error);
            return null;
        }
    } catch (error) {
        console.error('Failed to check system status:', error);
        return null;
    }
}

async function analyzeSymptoms(symptomsData) {
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(symptomsData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.results;
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        console.error('Symptom analysis failed:', error);
        throw error;
    }
}


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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
    
    .notification {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
`;
document.head.appendChild(style);

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateSymptoms,
        validateAge,
        checkSystemStatus,
        analyzeSymptoms
    };
}