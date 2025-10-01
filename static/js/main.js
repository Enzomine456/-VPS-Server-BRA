// ExitLag Free - Main JavaScript

// Global variables
let connectionCheckInterval;
let isConnected = false;

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize application
function initializeApp() {
    // Check if user is authenticated
    if (document.querySelector('[data-user-authenticated]')) {
        checkConnectionStatus();
        startConnectionMonitoring();
    }
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize form validations
    initializeFormValidations();
    
    // Initialize animations
    initializeAnimations();
}

// Connection Status Management
function checkConnectionStatus() {
    fetch('/api/status/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        updateConnectionUI(data);
    })
    .catch(error => {
        console.error('Error checking connection status:', error);
    });
}

function updateConnectionUI(data) {
    const statusBar = document.getElementById('connection-status');
    const statusText = document.getElementById('status-text');
    
    if (!statusBar || !statusText) return;
    
    if (data.connected) {
        isConnected = true;
        statusBar.className = 'bg-success text-white py-2';
        statusBar.classList.remove('d-none');
        statusText.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>
            Conectado ao ${data.server_name} (${data.server_city}, ${data.server_country}) - ${data.ping}ms
        `;
    } else {
        isConnected = false;
        statusBar.classList.add('d-none');
    }
}

function startConnectionMonitoring() {
    // Check connection status every 30 seconds
    connectionCheckInterval = setInterval(checkConnectionStatus, 30000);
}

function stopConnectionMonitoring() {
    if (connectionCheckInterval) {
        clearInterval(connectionCheckInterval);
    }
}

// Server Connection Functions
function connectToServer(serverId, serverName, serverPing = null) {
    showLoadingModal('Conectando...', 'Estabelecendo conexão com o servidor...');
    
    // Simulate ping measurement
    const pingBefore = serverPing ? Math.floor(Math.random() * 30) + serverPing : Math.floor(Math.random() * 100) + 50;
    
    const requestData = {
        ping_before: pingBefore
    };
    
    // Add game ID if present
    const gameId = getCurrentGameSelection();
    if (gameId) {
        requestData.game_id = gameId;
    }
    
    fetch(`/connect/${serverId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingModal();
        
        if (data.success) {
            showNotification('success', data.message);
            
            // Update connection status immediately
            isConnected = true;
            
            // Redirect after short delay
            setTimeout(() => {
                if (window.location.pathname !== '/dashboard/') {
                    window.location.href = '/dashboard/';
                } else {
                    window.location.reload();
                }
            }, 2000);
        } else {
            showNotification('danger', 'Erro ao conectar: ' + data.message);
        }
    })
    .catch(error => {
        hideLoadingModal();
        console.error('Connection error:', error);
        showNotification('danger', 'Erro de conexão. Tente novamente.');
    });
}

function disconnect() {
    if (!confirm('Desconectar do servidor atual?')) {
        return;
    }
    
    showLoadingModal('Desconectando...', 'Encerrando conexão...');
    
    fetch('/disconnect/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        }
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingModal();
        
        if (data.success) {
            showNotification('success', data.message);
            isConnected = false;
            
            // Redirect or reload
            setTimeout(() => {
                if (window.location.pathname === '/dashboard/') {
                    window.location.reload();
                } else {
                    window.location.href = '/dashboard/';
                }
            }, 1500);
        } else {
            showNotification('danger', 'Erro ao desconectar: ' + data.message);
        }
    })
    .catch(error => {
        hideLoadingModal();
        console.error('Disconnect error:', error);
        showNotification('danger', 'Erro de conexão. Tente novamente.');
    });
}

// UI Helper Functions
function showLoadingModal(title = 'Carregando...', message = 'Por favor aguarde...') {
    let modal = document.getElementById('loadingModal');
    
    if (!modal) {
        // Create loading modal if it doesn't exist
        modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'loadingModal';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-body text-center p-4">
                        <div class="spinner-border text-primary mb-3" role="status">
                            <span class="visually-hidden">Carregando...</span>
                        </div>
                        <h5 id="loadingTitle">${title}</h5>
                        <p id="loadingMessage" class="text-muted mb-0">${message}</p>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    } else {
        document.getElementById('loadingTitle').textContent = title;
        document.getElementById('loadingMessage').textContent = message;
    }
    
    const modalInstance = new bootstrap.Modal(modal, {
        backdrop: 'static',
        keyboard: false
    });
    modalInstance.show();
}

function hideLoadingModal() {
    const modal = document.getElementById('loadingModal');
    if (modal) {
        const modalInstance = bootstrap.Modal.getInstance(modal);
        if (modalInstance) {
            modalInstance.hide();
        }
    }
}

function showNotification(type, message, duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed slide-in-up`;
    alertDiv.style.cssText = 'top: 80px; right: 20px; z-index: 9999; max-width: 350px; min-width: 300px;';
    alertDiv.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${getIconForType(type)} me-2"></i>
            <div class="flex-grow-1">${message}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.classList.remove('show');
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 150);
        }
    }, duration);
}

function getIconForType(type) {
    const icons = {
        success: 'check-circle',
        danger: 'exclamation-triangle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Utility Functions
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

function getCurrentGameSelection() {
    const gameSelect = document.querySelector('[name="game_id"]');
    return gameSelect ? gameSelect.value : null;
}

function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
        return `${minutes}m ${secs}s`;
    } else {
        return `${secs}s`;
    }
}

function formatPing(ping) {
    if (ping < 30) return { value: ping, class: 'text-success', label: 'Excelente' };
    if (ping < 60) return { value: ping, class: 'text-primary', label: 'Bom' };
    if (ping < 100) return { value: ping, class: 'text-warning', label: 'Regular' };
    return { value: ping, class: 'text-danger', label: 'Alto' };
}

// Form Validations
function initializeFormValidations() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Smooth Scrolling
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
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
}

// Animations
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with animation class
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));
}

// Performance Monitoring
function measurePing(hostname = 'google.com') {
    return new Promise((resolve) => {
        const start = performance.now();
        const img = new Image();
        
        img.onload = img.onerror = () => {
            const ping = Math.round(performance.now() - start);
            resolve(ping);
        };
        
        img.src = `https://${hostname}/favicon.ico?${Date.now()}`;
        
        // Fallback timeout
        setTimeout(() => resolve(Math.floor(Math.random() * 50) + 30), 5000);
    });
}

// Game Optimization
function optimizeForGame(gameName, gameId) {
    showLoadingModal('Otimizando...', `Configurando otimização para ${gameName}...`);
    
    // Simulate server recommendation
    setTimeout(() => {
        hideLoadingModal();
        
        // Show game optimization modal
        showGameOptimizationModal(gameName, gameId);
    }, 1500);
}

function showGameOptimizationModal(gameName, gameId) {
    let modal = document.getElementById('gameOptimizationModal');
    
    if (!modal) {
        modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'gameOptimizationModal';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-rocket me-2"></i>
                            Otimização para <span id="gameNameModal"></span>
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="text-center mb-4">
                            <i class="fas fa-gamepad fa-3x text-primary mb-3"></i>
                            <p>Servidores recomendados para melhor performance:</p>
                        </div>
                        <div id="recommendedServersList">
                            <!-- Servers will be loaded here -->
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
    
    document.getElementById('gameNameModal').textContent = gameName;
    
    // Load recommended servers
    loadRecommendedServers(gameId);
    
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
}

function loadRecommendedServers(gameId) {
    const serversList = document.getElementById('recommendedServersList');
    serversList.innerHTML = '<div class="text-center"><div class="spinner-border text-primary"></div></div>';
    
    // Simulate server loading
    setTimeout(() => {
        const servers = [
            { id: 1, name: 'Brasil São Paulo', ping: 25, country: '🇧🇷', load: 35 },
            { id: 2, name: 'Brasil Rio de Janeiro', ping: 30, country: '🇧🇷', load: 42 },
            { id: 3, name: 'Argentina Buenos Aires', ping: 45, country: '🇦🇷', load: 28 }
        ];
        
        let serversHtml = '<div class="list-group">';
        servers.forEach(server => {
            const pingFormat = formatPing(server.ping);
            serversHtml += `
                <button class="list-group-item list-group-item-action d-flex justify-content-between align-items-center" 
                        onclick="connectToServerFromGame(${server.id}, '${server.name}', ${gameId})">
                    <div>
                        <span class="me-2">${server.country}</span>
                        <strong>${server.name}</strong>
                        <br>
                        <small class="text-muted">Carga: ${server.load}%</small>
                    </div>
                    <div class="text-end">
                        <span class="badge ${pingFormat.class.replace('text-', 'bg-')} mb-1">${server.ping}ms</span>
                        <br>
                        <small class="${pingFormat.class}">${pingFormat.label}</small>
                    </div>
                </button>
            `;
        });
        serversHtml += '</div>';
        
        serversList.innerHTML = serversHtml;
    }, 1000);
}

function connectToServerFromGame(serverId, serverName, gameId) {
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('gameOptimizationModal'));
    modal.hide();
    
    // Connect with game optimization
    connectToServer(serverId, serverName);
}

// Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    
    // Show user-friendly error message for critical errors
    if (e.error && e.error.message.includes('fetch')) {
        showNotification('warning', 'Problema de conexão detectado. Tentando reconectar...');
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    stopConnectionMonitoring();
});

// Export functions for global access
window.ExitLagFree = {
    connectToServer,
    disconnect,
    checkConnectionStatus,
    showNotification,
    optimizeForGame,
    measurePing
};