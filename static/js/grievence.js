document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('grievance-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(form);
            const successMessage = document.getElementById('success-message');

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    form.reset();
                    successMessage.classList.remove('hidden');
                    setTimeout(() => {
                        window.location.href = '/dashboard'; 
                    }, 2000);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
