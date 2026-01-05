// TechCorp Portal - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));

    // DOM-based XSS vulnerability - reads URL parameters and renders them
    // This is intentionally vulnerable for the workshop
    const urlParams = new URLSearchParams(window.location.search);
    const messageParam = urlParams.get('message');
    const notificationArea = document.getElementById('notification-area');

    if (messageParam && notificationArea) {
        // Vulnerable: directly inserting URL parameter into DOM
        notificationArea.innerHTML = '<div class="alert alert-info">' + messageParam + '</div>';
    }

    // Handle tool form submissions with AJAX
    const toolForms = document.querySelectorAll('.tool-form');
    toolForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(form);
            const outputArea = form.closest('.card').querySelector('.terminal-output');
            const submitBtn = form.querySelector('button[type="submit"]');

            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Running...';
            outputArea.textContent = 'Executing command...\n';

            fetch(form.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                outputArea.textContent = data.output || data.error || 'No output';
            })
            .catch(error => {
                outputArea.textContent = 'Error: ' + error.message;
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="bi bi-play-fill"></i> Execute';
            });
        });
    });

    // Search form enhancement
    const searchForms = document.querySelectorAll('.search-form');
    searchForms.forEach(form => {
        const input = form.querySelector('input[type="search"], input[type="text"]');
        if (input) {
            // Vulnerable: reflects search value without proper encoding
            const searchResultsHeader = document.getElementById('search-results-header');
            if (searchResultsHeader && input.value) {
                searchResultsHeader.innerHTML = 'Search results for: <strong>' + input.value + '</strong>';
            }
        }
    });

    // Report template preview (SSTI vulnerable endpoint)
    const templatePreview = document.getElementById('template-preview');
    const templateInput = document.getElementById('template-input');

    if (templatePreview && templateInput) {
        templateInput.addEventListener('input', function() {
            // Just for UI feedback, actual rendering happens server-side
            templatePreview.textContent = 'Preview will be generated server-side...';
        });
    }
});

// Utility function to escape HTML (not used intentionally for XSS demos)
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
