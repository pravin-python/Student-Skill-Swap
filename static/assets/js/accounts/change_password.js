// Show Password Modal
function showPasswordModal() {
    const modal = new bootstrap.Modal(document.getElementById('passwordModal'));
    modal.show();
}

// Changing password for a user 
function changePassword() {
    const form = document.getElementById('passwordForm');
    const formData = new FormData(form);

    // Clear previous errors
    document.querySelectorAll('#passwordForm .form-control').forEach(input => {
    input.classList.remove('is-invalid');
    const feedback = input.parentElement.querySelector('.invalid-feedback');
    if (feedback) feedback.textContent = '';  // clear old messages
    });


    let hasError = false;

    // Get values
    const currentPassword = formData.get('current_password').trim();
    const newPassword = formData.get('new_password').trim();
    const confirmPassword = formData.get('confirm_password').trim();

    // Empty field checks
    if (!currentPassword) {
        const input = document.querySelector('[name="current_password"]');
        input.classList.add('is-invalid');
        const feedback = input.parentElement.querySelector('.invalid-feedback');
        if (feedback) feedback.textContent = 'Current Password is required';
        hasError = true;
    }

    if (!newPassword) {
        const input = document.querySelector('[name="new_password"]');
        input.classList.add('is-invalid');
        const feedback = input.parentElement.querySelector('.invalid-feedback');
        if (feedback) feedback.textContent = 'New Password is required';
        hasError = true;
    }

    if (!confirmPassword) {
        const input = document.querySelector('[name="confirm_password"]');
        input.classList.add('is-invalid');
        const feedback = input.parentElement.querySelector('.invalid-feedback');
        if (feedback) feedback.textContent = 'Confirm Password is required';
        hasError = true;
    }

    // Only check match if both new & confirm filled
    if (newPassword && confirmPassword && newPassword !== confirmPassword) {
        const input = document.querySelector('[name="confirm_password"]');
        input.classList.add('is-invalid');
        const feedback = input.parentElement.querySelector('.invalid-feedback');
        if (feedback) feedback.textContent = 'Passwords do not match';
        hasError = true;
    }

    // Stop if any validation failed
    if (hasError) {
        return;
    }

    // API call
    fetch(form.dataset.url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const modal = bootstrap.Modal.getInstance(document.getElementById('passwordModal'));
            modal.hide();
            showAlert('Password changed successfully!', 'success');
            form.reset();
        } else {
            // Show specific errors
            Object.keys(data.errors || {}).forEach(field => {
                const input = document.querySelector(`[name="${field}"]`);
                if (input) {
                    input.classList.add('is-invalid');
                    const feedback = input.parentElement.querySelector('.invalid-feedback');
                    if (feedback) {
                        feedback.textContent = data.errors[field];
                    }
                }
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred. Please try again.', 'danger');
    });
}