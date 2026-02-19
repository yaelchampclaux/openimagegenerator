/**
 * Provider Health Check UI Component
 * Add this to your generator.html template
 */

// Health Check Manager
const HealthCheckManager = {
    checkInterval: null,
    lastCheck: null,
    
    /**
     * Initialize health checking
     */
    init() {
        this.checkHealth();
        // Check health every 5 minutes
        this.checkInterval = setInterval(() => this.checkHealth(), 5 * 60 * 1000);
        
        // Add UI elements
        this.addHealthStatusUI();
    },
    
    /**
     * Perform health check via API
     */
    async checkHealth() {
        try {
            const response = await fetch('/api/health/');
            const data = await response.json();
            
            if (data.success) {
                this.lastCheck = new Date();
                this.updateHealthUI(data);
                this.updateProviderDropdown(data);
            }
        } catch (error) {
            console.error('Health check failed:', error);
        }
    },
    
    /**
     * Add health status UI to page
     */
    addHealthStatusUI() {
        // Create health status container
        const container = document.createElement('div');
        container.id = 'health-status-container';
        container.className = 'health-status-container';
        container.innerHTML = `
            <div class="health-status-header">
                <span class="health-status-title">🔍 Provider Status</span>
                <button class="health-refresh-btn" onclick="HealthCheckManager.checkHealth()">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41zm-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9z"/>
                        <path fill-rule="evenodd" d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5.002 5.002 0 0 0 8 3zM3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9H3.1z"/>
                    </svg>
                    Refresh
                </button>
            </div>
            <div id="health-status-content" class="health-status-content">
                <div class="health-loading">Checking providers...</div>
            </div>
            <div id="health-recommendations" class="health-recommendations"></div>
        `;
        
        // Insert before the form or at top of page
        const form = document.querySelector('.generation-form') || document.body;
        form.parentNode.insertBefore(container, form);
        
        // Add styles
        this.addStyles();
    },
    
    /**
     * Update health status UI
     */
    updateHealthUI(data) {
        const content = document.getElementById('health-status-content');
        const { providers, summary } = data;
        
        let html = `
            <div class="health-summary">
                <span class="health-stat">
                    <span class="stat-label">Total:</span>
                    <span class="stat-value">${summary.total}</span>
                </span>
                <span class="health-stat health-working">
                    <span class="stat-label">Working:</span>
                    <span class="stat-value">${summary.working}</span>
                </span>
                ${summary.broken > 0 ? `
                <span class="health-stat health-broken">
                    <span class="stat-label">Broken:</span>
                    <span class="stat-value">${summary.broken}</span>
                </span>
                ` : ''}
            </div>
            <div class="health-providers">
        `;
        
        for (const [key, provider] of Object.entries(providers)) {
            const statusClass = provider.is_healthy ? 'status-working' : 'status-broken';
            const statusIcon = provider.is_healthy ? '✅' : '❌';
            const keyIcon = provider.info.requires_api_key 
                ? (provider.info.has_api_key ? '🔑' : '⚠️') 
                : '🆓';
            
            html += `
                <div class="provider-status ${statusClass}">
                    <div class="provider-header">
                        <span class="provider-name">
                            ${keyIcon} ${provider.info.name}
                        </span>
                        <span class="provider-status-badge">
                            ${statusIcon} ${provider.is_healthy ? 'Working' : 'Broken'}
                        </span>
                    </div>
                    <div class="provider-details">
                        <small>${provider.message}</small>
                        ${provider.response_time > 0 ? `
                            <small class="response-time">⚡ ${provider.response_time.toFixed(2)}s</small>
                        ` : ''}
                    </div>
                    ${!provider.is_healthy && provider.info.requires_api_key && !provider.info.has_api_key ? `
                        <div class="provider-fix">
                            <small>💡 Fix: Add API key in .env file</small>
                        </div>
                    ` : ''}
                </div>
            `;
        }
        
        html += '</div>';
        content.innerHTML = html;
        
        // Update recommendations
        this.updateRecommendations(data.recommendations);
    },
    
    /**
     * Update recommendations section
     */
    updateRecommendations(recommendations) {
        const container = document.getElementById('health-recommendations');
        
        if (!recommendations || recommendations.length === 0) {
            container.style.display = 'none';
            return;
        }
        
        container.style.display = 'block';
        
        let html = '<div class="recommendations-title">💡 Recommendations</div>';
        
        for (const rec of recommendations) {
            const priorityClass = `priority-${rec.priority}`;
            html += `
                <div class="recommendation ${priorityClass}">
                    <div class="rec-message">${rec.message}</div>
                    ${rec.action ? `
                        <div class="rec-action">→ ${rec.action}</div>
                    ` : ''}
                    ${rec.steps ? `
                        <ol class="rec-steps">
                            ${rec.steps.map(step => `<li>${step}</li>`).join('')}
                        </ol>
                    ` : ''}
                    ${rec.fix_url ? `
                        <div class="rec-link">
                            <a href="${rec.fix_url}" target="_blank">
                                Open ${rec.fix_url} →
                            </a>
                        </div>
                    ` : ''}
                </div>
            `;
        }
        
        container.innerHTML = html;
    },
    
    /**
     * Update provider dropdown to show status
     */
    updateProviderDropdown(data) {
        const dropdown = document.getElementById('provider');
        if (!dropdown) return;
        
        const { providers } = data;
        
        // Add status indicators to options
        Array.from(dropdown.options).forEach(option => {
            const providerId = option.value;
            const provider = providers[providerId];
            
            if (provider) {
                const status = provider.is_healthy ? '✅' : '❌';
                const originalText = option.text.replace(/^[✅❌]\s+/, '');
                option.text = `${status} ${originalText}`;
                
                // Disable broken providers
                if (!provider.is_healthy) {
                    option.disabled = true;
                    option.title = provider.message;
                }
            }
        });
        
        // Auto-select first working provider
        const workingProviders = Object.entries(providers)
            .filter(([_, p]) => p.is_healthy)
            .map(([key, _]) => key);
        
        if (workingProviders.length > 0 && !dropdown.value) {
            // Prefer pollinations or gemini
            const preferred = workingProviders.includes('pollinations') 
                ? 'pollinations' 
                : workingProviders[0];
            dropdown.value = preferred;
        }
    },
    
    /**
     * Add CSS styles
     */
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .health-status-container {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 16px;
                margin: 20px 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
            
            .health-status-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }
            
            .health-status-title {
                font-weight: 600;
                font-size: 16px;
            }
            
            .health-refresh-btn {
                display: flex;
                align-items: center;
                gap: 4px;
                padding: 6px 12px;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                cursor: pointer;
                font-size: 13px;
                transition: all 0.2s;
            }
            
            .health-refresh-btn:hover {
                background: #e9ecef;
            }
            
            .health-summary {
                display: flex;
                gap: 16px;
                padding: 12px;
                background: white;
                border-radius: 6px;
                margin-bottom: 12px;
            }
            
            .health-stat {
                display: flex;
                flex-direction: column;
                gap: 4px;
            }
            
            .stat-label {
                font-size: 12px;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .stat-value {
                font-size: 24px;
                font-weight: 700;
            }
            
            .health-working .stat-value {
                color: #28a745;
            }
            
            .health-broken .stat-value {
                color: #dc3545;
            }
            
            .health-providers {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 12px;
            }
            
            .provider-status {
                background: white;
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 12px;
                transition: all 0.2s;
            }
            
            .provider-status.status-working {
                border-color: #28a745;
            }
            
            .provider-status.status-broken {
                border-color: #dc3545;
                opacity: 0.7;
            }
            
            .provider-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            }
            
            .provider-name {
                font-weight: 600;
                font-size: 14px;
            }
            
            .provider-status-badge {
                font-size: 12px;
                padding: 2px 8px;
                border-radius: 12px;
                background: #f8f9fa;
            }
            
            .provider-details {
                font-size: 12px;
                color: #6c757d;
                display: flex;
                flex-direction: column;
                gap: 4px;
            }
            
            .response-time {
                color: #28a745;
                font-weight: 600;
            }
            
            .provider-fix {
                margin-top: 8px;
                padding: 8px;
                background: #fff3cd;
                border-radius: 4px;
                font-size: 12px;
                color: #856404;
            }
            
            .health-recommendations {
                margin-top: 16px;
                padding: 12px;
                background: #e7f3ff;
                border: 1px solid #b3d9ff;
                border-radius: 6px;
            }
            
            .recommendations-title {
                font-weight: 600;
                margin-bottom: 12px;
            }
            
            .recommendation {
                padding: 12px;
                background: white;
                border-left: 4px solid #0d6efd;
                border-radius: 4px;
                margin-bottom: 12px;
            }
            
            .recommendation.priority-high {
                border-left-color: #dc3545;
            }
            
            .recommendation.priority-medium {
                border-left-color: #ffc107;
            }
            
            .rec-message {
                font-weight: 600;
                margin-bottom: 8px;
            }
            
            .rec-action {
                font-size: 13px;
                color: #6c757d;
                margin-bottom: 8px;
            }
            
            .rec-steps {
                margin: 8px 0;
                padding-left: 20px;
                font-size: 13px;
            }
            
            .rec-link a {
                color: #0d6efd;
                text-decoration: none;
                font-weight: 500;
            }
            
            .rec-link a:hover {
                text-decoration: underline;
            }
            
            .health-loading {
                text-align: center;
                padding: 20px;
                color: #6c757d;
            }
        `;
        document.head.appendChild(style);
    }
};

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => HealthCheckManager.init());
} else {
    HealthCheckManager.init();
}

// Add to template:
/*
{% block extra_js %}
<script src="{% static 'js/health_check.js' %}"></script>
{% endblock %}
*/
