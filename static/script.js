// static/script.js - Enhanced JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const emailForm = document.getElementById('emailForm');
    const emailTextarea = document.getElementById('emailText');
    const checkBtn = document.getElementById('checkBtn');
    const clearBtn = document.getElementById('clearBtn');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceValue = document.getElementById('confidenceValue');
    
    // Sample emails for quick testing
    const sampleEmails = {
        phishing: "URGENT: Your account has been compromised!\n\nDear Valued Customer,\n\nWe have detected unusual activity on your account. To secure your account, please click the link below immediately:\n\nhttp://bit.ly/fake-bank-login\n\nEnter your username, password, and Social Security Number to verify your identity.\n\nThis is URGENT! Failure to respond within 24 hours will result in account suspension.\n\nBest regards,\nSecurity Team",
        
        legitimate: "Meeting Agenda for Tomorrow\n\nHi Team,\n\nHere's the agenda for our meeting tomorrow at 10:00 AM in Conference Room B:\n\n1. Project updates\n2. Q3 goals review\n3. Team feedback session\n4. Action items\n\nPlease come prepared with your updates. Let me know if you have any items to add.\n\nBest,\nJohn Doe\nProject Manager",
        
        suspicious: "Congratulations! You've Won $1000 Gift Card!\n\nYou've been selected as our lucky winner! Click below to claim your $1000 Walmart gift card:\n\nhttp://win-gift.xyz/claim-now\n\nHurry! This offer expires in 2 hours.\n\nNo purchase necessary. Limited time offer."
    };
    
    // Initialize
    init();
    
    function init() {
        // Add event listeners
        emailForm.addEventListener('submit', handleSubmit);
        clearBtn.addEventListener('click', clearForm);
        
        // Add sample email buttons dynamically
        addSampleEmailButtons();
        
        // Add character counter
        addCharacterCounter();
        
        // Add auto-save feature
        autoSaveEmailContent();
        
        // Restore saved content if exists
        restoreSavedContent();
    }
    
    function handleSubmit(event) {
        event.preventDefault();
        
        const emailText = emailTextarea.value.trim();
        
        if (!emailText) {
            showError('Please enter some email text to analyze.');
            return;
        }
        
        if (emailText.length < 10) {
            showError('Email text is too short. Please enter at least 10 characters.');
            return;
        }
        
        // Show loading animation
        showLoading();
        
        // Store the email for potential analysis
        localStorage.setItem('lastEmail', emailText);
        updateStats();
        
        // The form will submit normally, but we add visual feedback
        setTimeout(() => {
            hideLoading();
            // Scroll to result if it exists
            if (resultDiv) {
                resultDiv.scrollIntoView({ behavior: 'smooth' });
            }
        }, 1000);
    }
    
    function clearForm() {
        if (confirm('Are you sure you want to clear the email text?')) {
            emailTextarea.value = '';
            localStorage.removeItem('savedEmail');
            emailTextarea.focus();
            
            // Show success message
            showToast('Email text cleared successfully!', 'success');
        }
    }
    
    function loadSampleEmail(type) {
        if (sampleEmails[type]) {
            emailTextarea.value = sampleEmails[type];
            emailTextarea.focus();
            
            // Update character count
            updateCharacterCount();
            
            // Show message
            const typeName = type.charAt(0).toUpperCase() + type.slice(1);
            showToast(`Loaded ${typeName} sample email`, 'info');
        }
    }
    
    function addSampleEmailButtons() {
        const buttonGroup = document.querySelector('.button-group');
        if (!buttonGroup) return;
        
        const sampleContainer = document.createElement('div');
        sampleContainer.className = 'sample-buttons';
        sampleContainer.innerHTML = `
            <p style="margin: 15px 0 10px; color: #666; font-weight: 500;">
                <i class="fas fa-vial"></i> Try Sample Emails:
            </p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button type="button" class="sample-btn phishing-sample" style="background: #ff6b6b;">
                    <i class="fas fa-skull-crossbones"></i> Phishing Example
                </button>
                <button type="button" class="sample-btn suspicious-sample" style="background: #ff922b;">
                    <i class="fas fa-exclamation-triangle"></i> Suspicious Example
                </button>
                <button type="button" class="sample-btn legitimate-sample" style="background: #51cf66;">
                    <i class="fas fa-check-circle"></i> Legitimate Example
                </button>
            </div>
        `;
        
        buttonGroup.parentNode.insertBefore(sampleContainer, buttonGroup.nextSibling);
        
        // Add event listeners to sample buttons
        document.querySelector('.phishing-sample').addEventListener('click', () => loadSampleEmail('phishing'));
        document.querySelector('.suspicious-sample').addEventListener('click', () => loadSampleEmail('suspicious'));
        document.querySelector('.legitimate-sample').addEventListener('click', () => loadSampleEmail('legitimate'));
    }
    
    function addCharacterCounter() {
        const counter = document.createElement('div');
        counter.id = 'charCounter';
        counter.style.cssText = 'text-align: right; margin-top: 5px; color: #666; font-size: 0.9rem;';
        
        emailTextarea.parentNode.insertBefore(counter, emailTextarea.nextSibling);
        
        emailTextarea.addEventListener('input', updateCharacterCount);
        updateCharacterCount();
    }
    
    function updateCharacterCount() {
        const counter = document.getElementById('charCounter');
        if (!counter) return;
        
        const count = emailTextarea.value.length;
        const words = emailTextarea.value.trim().split(/\s+/).filter(w => w.length > 0).length;
        
        counter.innerHTML = `
            <span class="tooltip">
                ${count} characters, ${words} words
                <span class="tooltiptext">Email analysis works best with 50-5000 characters</span>
            </span>
        `;
        
        // Color code based on length
        if (count < 50) {
            counter.style.color = '#e74c3c';
        } else if (count > 5000) {
            counter.style.color = '#f39c12';
        } else {
            counter.style.color = '#27ae60';
        }
    }
    
    function autoSaveEmailContent() {
        let saveTimeout;
        
        emailTextarea.addEventListener('input', function() {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                localStorage.setItem('savedEmail', this.value);
            }, 1000);
        });
    }
    
    function restoreSavedContent() {
        const savedEmail = localStorage.getItem('savedEmail');
        if (savedEmail && !emailTextarea.value) {
            if (confirm('Found a previously saved email. Would you like to restore it?')) {
                emailTextarea.value = savedEmail;
                updateCharacterCount();
                showToast('Email content restored from previous session.', 'info');
            }
        }
    }
    
    function showLoading() {
        if (loadingDiv) {
            loadingDiv.style.display = 'block';
            checkBtn.disabled = true;
            checkBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        }
    }
    
    function hideLoading() {
        if (loadingDiv) {
            loadingDiv.style.display = 'none';
            checkBtn.disabled = false;
            checkBtn.innerHTML = '<i class="fas fa-search"></i> Check Email';
        }
    }
    
    function showError(message) {
        showToast(message, 'error');
        // Add shake animation to form
        emailForm.style.animation = 'shake 0.5s';
        setTimeout(() => {
            emailForm.style.animation = '';
        }, 500);
    }
    
    function showToast(message, type = 'info') {
        // Remove existing toast
        const existingToast = document.querySelector('.toast');
        if (existingToast) {
            existingToast.remove();
        }
        
        // Create new toast
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="fas fa-${getToastIcon(type)}"></i>
            <span>${message}</span>
            <button class="toast-close"><i class="fas fa-times"></i></button>
        `;
        
        // Add styles
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${getToastColor(type)};
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 1000;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            animation: slideInRight 0.3s ease-out;
            max-width: 400px;
        `;
        
        document.body.appendChild(toast);
        
        // Add close button functionality
        toast.querySelector('.toast-close').addEventListener('click', () => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        });
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    }
    
    function getToastIcon(type) {
        switch(type) {
            case 'success': return 'check-circle';
            case 'error': return 'exclamation-circle';
            case 'warning': return 'exclamation-triangle';
            default: return 'info-circle';
        }
    }
    
    function getToastColor(type) {
        switch(type) {
            case 'success': return 'linear-gradient(135deg, #51cf66 0%, #2b8a3e 100%)';
            case 'error': return 'linear-gradient(135deg, #ff6b6b 0%, #c92a2a 100%)';
            case 'warning': return 'linear-gradient(135deg, #ff922b 0%, #e8590c 100%)';
            default: return 'linear-gradient(135deg, #4dabf7 0%, #1971c2 100%)';
        }
    }
    
    function updateStats() {
        const stats = {
            checks: parseInt(localStorage.getItem('totalChecks') || '0') + 1,
            phishing: parseInt(localStorage.getItem('phishingCount') || '0'),
            legitimate: parseInt(localStorage.getItem('legitimateCount') || '0')
        };
        
        // This would be updated based on actual results
        // For now, just increment total checks
        localStorage.setItem('totalChecks', stats.checks);
        
        // Update stats display if it exists
        const statsElement = document.querySelector('.stats');
        if (statsElement) {
            statsElement.innerHTML = `
                <div class="stat-item">
                    <div class="stat-value">${stats.checks}</div>
                    <div class="stat-label">Total Checks</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${stats.phishing}</div>
                    <div class="stat-label">Phishing Detected</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${stats.legitimate}</div>
                    <div class="stat-label">Legitimate Emails</div>
                </div>
            `;
        }
    }
    
    // Add some CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        
        .sample-btn {
            padding: 10px 15px;
            border: none;
            border-radius: 8px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            flex: 1;
        }
        
        .sample-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .toast-close {
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            padding: 0;
            margin-left: 10px;
        }
    `;
    document.head.appendChild(style);
});