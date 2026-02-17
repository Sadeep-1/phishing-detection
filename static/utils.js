// static/utils.js - Utility functions
const Utils = {
    // Format confidence value with color
    formatConfidence(confidence) {
        if (confidence >= 80) return `<span style="color: #e74c3c; font-weight: bold;">${confidence}% (High Risk)</span>`;
        if (confidence >= 60) return `<span style="color: #f39c12; font-weight: bold;">${confidence}% (Medium Risk)</span>`;
        return `<span style="color: #27ae60; font-weight: bold;">${confidence}% (Low Risk)</span>`;
    },
    
    // Get risk level description
    getRiskDescription(confidence) {
        if (confidence >= 80) {
            return {
                level: 'High',
                icon: '🔥',
                description: 'Multiple phishing indicators detected. Exercise extreme caution.'
            };
        } else if (confidence >= 60) {
            return {
                level: 'Medium',
                icon: '⚠️',
                description: 'Some suspicious elements found. Verify the sender.'
            };
        } else {
            return {
                level: 'Low',
                icon: '✅',
                description: 'Appears legitimate, but always stay vigilant.'
            };
        }
    },
    
    // Save analysis history
    saveToHistory(email, result, confidence) {
        const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
        history.unshift({
            email: email.substring(0, 100) + (email.length > 100 ? '...' : ''),
            result: result,
            confidence: confidence,
            timestamp: new Date().toISOString()
        });
        
        // Keep only last 50 entries
        if (history.length > 50) {
            history.pop();
        }
        
        localStorage.setItem('analysisHistory', JSON.stringify(history));
    },
    
    // Get analysis history
    getHistory() {
        return JSON.parse(localStorage.getItem('analysisHistory') || '[]');
    },
    
    // Clear history
    clearHistory() {
        localStorage.removeItem('analysisHistory');
    },
    
    // Export results as CSV
    exportResults() {
        const history = this.getHistory();
        if (history.length === 0) {
            alert('No analysis history to export.');
            return;
        }
        
        let csv = 'Timestamp,Email Preview,Result,Confidence\n';
        history.forEach(item => {
            const timestamp = new Date(item.timestamp).toLocaleString();
            const email = item.email.replace(/"/g, '""');
            csv += `"${timestamp}","${email}","${item.result}","${item.confidence}"\n`;
        });
        
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `phishing-analysis-${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    },
    
    // Calculate statistics
    getStatistics() {
        const history = this.getHistory();
        const stats = {
            total: history.length,
            phishing: history.filter(h => h.result.includes('PHISHING')).length,
            legitimate: history.filter(h => h.result.includes('LEGITIMATE')).length,
            errors: history.filter(h => h.result.includes('Error')).length
        };
        
        stats.phishingPercentage = stats.total > 0 ? ((stats.phishing / stats.total) * 100).toFixed(1) : 0;
        stats.legitimatePercentage = stats.total > 0 ? ((stats.legitimate / stats.total) * 100).toFixed(1) : 0;
        
        return stats;
    }
};