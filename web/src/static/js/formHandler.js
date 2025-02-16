document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('plotForm');
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorMessage = document.getElementById('error-message');
    const plotImage = document.getElementById('plot-image');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading spinner and hide error/image
        loadingSpinner.style.display = 'flex';
        errorMessage.style.display = 'none';
        plotImage.style.display = 'none';
        
        const textContent = document.getElementById('text_content').value;
        
        try {
            const response = await fetch('/api/generate-plot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text_content: textContent })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Hide loading spinner and show image
                loadingSpinner.style.display = 'none';
                plotImage.src = data.plot_url;
                plotImage.style.display = 'block';
            } else {
                // Show error message
                errorMessage.textContent = data.error || 'Si è verificato un errore durante la generazione del plot';
                errorMessage.style.display = 'block';
                loadingSpinner.style.display = 'none';
            }
        } catch (error) {
            // Handle network errors
            errorMessage.textContent = 'Errore di rete durante la richiesta';
            errorMessage.style.display = 'block';
            loadingSpinner.style.display = 'none';
        }
    });
});