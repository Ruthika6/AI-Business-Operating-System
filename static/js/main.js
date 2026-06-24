// FlowZint AI General UI Utility Handlers

// Toast Notification Manager
function showToast(message, type = "success") {
    // Check if container exists, otherwise create it
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.className = "fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm pointer-events-none";
        document.body.appendChild(container);
    }

    // Create toast element
    const toast = document.createElement("div");
    toast.className = `glass-panel px-5 py-3 rounded-lg flex items-center gap-3 transform translate-y-5 opacity-0 transition-all duration-300 pointer-events-auto shadow-2xl`;
    
    // Set colors based on type
    let icon = "fa-check-circle";
    let iconColor = "text-emerald-400";
    let borderAccent = "border-l-4 border-emerald-500";
    
    if (type === "error") {
        icon = "fa-exclamation-circle";
        iconColor = "text-rose-400";
        borderAccent = "border-l-4 border-rose-500";
    } else if (type === "warning") {
        icon = "fa-exclamation-triangle";
        iconColor = "text-amber-400";
        borderAccent = "border-l-4 border-amber-500";
    } else if (type === "info") {
        icon = "fa-info-circle";
        iconColor = "text-cyan-400";
        borderAccent = "border-l-4 border-cyan-500";
    }
    
    toast.className += ` ${borderAccent}`;
    toast.innerHTML = `
        <i class="fas ${icon} ${iconColor} text-lg"></i>
        <div class="text-sm font-medium text-slate-200">${message}</div>
        <button class="ml-auto text-slate-400 hover:text-slate-200 text-xs focus:outline-none" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    container.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.classList.remove("translate-y-5", "opacity-0");
    }, 50);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.classList.add("translate-y-5", "opacity-0");
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 4000);
}

// Global API Fetch wrapper with unified error trapping
async function apiFetch(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || data.error || `HTTP Error ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error(`API Fetch Error [${url}]:`, error);
        showToast(error.message || "An unexpected error occurred", "error");
        throw error;
    }
}

// Simple HTML Escaper to prevent XSS in client-side renders
function escapeHTML(str) {
    if (!str) return '';
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Formatting Utilities
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
}
