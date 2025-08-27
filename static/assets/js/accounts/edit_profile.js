// Script For editing a profile 
let editMode = false;

function enableEditMode() {
    editMode = true;
    document.getElementById('editButtons').style.display = 'block';
    
    // Enable all form inputs except username and email
    document.querySelectorAll('.profile-input').forEach(input => {
        if (input.name !== 'username') {
            input.removeAttribute('readonly');
            input.removeAttribute('disabled');
        }
    });
    
    // Change button text
    document.querySelector('button[onclick="enableEditMode()"]').innerHTML = 
        '<i class="bi bi-pencil"></i> Editing...';
    document.querySelector('button[onclick="enableEditMode()"]').disabled = true;
}

// When click on cancel button 
function cancelEdit() {
    location.reload(); // Simple way to reset form
}

// After click on save changes 
function saveProfile() {
    const form = document.getElementById('profileForm');
    const formData = new FormData(form);
    
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
            showAlert('Profile updated successfully!', 'success');
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            showAlert('Error updating profile. Please check your inputs.', 'danger');
            // Show specific errors
            Object.keys(data.errors || {}).forEach(field => {
                const input = document.querySelector(`[name="${field}"]`);
                if (input) {
                    input.classList.add('is-invalid');
                    const feedback = input.nextElementSibling;
                    if (feedback && feedback.classList.contains('invalid-feedback')) {
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

// Previewing image when editing a profile 
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profileImage').src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}