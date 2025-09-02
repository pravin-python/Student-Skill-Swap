// Request management functions
function acceptRequest(requestId) {
    if (confirm('Accept this learning request?')) {
        makeRequest('POST', `/courses/accept_request/${requestId}/`, null, 'Request accepted successfully!');
    }
}

function rejectRequest(requestId) {
    document.getElementById('rejectionRequestId').value = requestId;
    document.getElementById('rejectionType').value = 'reject';
    document.getElementById('rejectionModalTitle').textContent = 'Reject Learning Request';
    document.getElementById('rejectionForm').reset();
    
    const modal = new bootstrap.Modal(document.getElementById('rejectionModal'));
    modal.show();
}

function cancelRequest(requestId) {
    document.getElementById('rejectionRequestId').value = requestId;
    document.getElementById('rejectionType').value = 'cancel';
    document.getElementById('rejectionModalTitle').textContent = 'Cancel Learning Request';
    document.getElementById('rejectionForm').reset();
    
    const modal = new bootstrap.Modal(document.getElementById('rejectionModal'));
    modal.show();
}

function deleteRequest(requestId) {
    if (confirm('Delete this request permanently?')) {
        makeRequest('POST', `/courses/delete_request/${requestId}/`, null, 'Request deleted.');
    }
}

function submitRejection() {
    const form = document.getElementById('rejectionForm');
    const formData = new FormData(form);
    
    if (!formData.get('reason').trim()) {
        alert('Please provide a reason for this action.');
        return;
    }
    
    const requestId = formData.get('request_id');
    const actionType = formData.get('action_type');
    
    let url, successMessage;
    if (actionType === 'reject') {
        url = `/courses/reject_request/${requestId}/`;
        successMessage = 'Request rejected successfully.';
    } else {
        url = `/courses/cancel_request/${requestId}/`;
        successMessage = 'Request cancelled successfully.';
    }
    
    // Send form data instead of JSON
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(successMessage);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('rejectionModal'));
    modal.hide();
}

// Session modal functions
function openSessionModal(requestId) {
    document.getElementById('sessionRequestId').value = requestId;
    document.getElementById('sessionForm').reset();
    document.getElementById('sessionRequestId').value = requestId; // Reset clears this too
    
    // Set minimum date to today
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('sessionDate').min = now.toISOString().slice(0, 16);
    
    const modal = new bootstrap.Modal(document.getElementById('sessionModal'));
    modal.show();
}

function createSession() {
    const form = document.getElementById('sessionForm');
    
    // Clear previous validation errors
    clearValidationErrors();
    
    // Validate form
    if (!validateSessionForm()) {
        return;
    }
    
    const formData = new FormData(form);
    
    // Add CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);
    
    fetch('/courses/create_session/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const modal = bootstrap.Modal.getInstance(document.getElementById('sessionModal'));
            modal.hide();
            alert(data.message);
            location.reload();
        } else {
            if (data.errors) {
                displayValidationErrors(data.errors);
            } else {
                alert(data.message);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while creating the session.');
    });
}

function validateSessionForm() {
    let isValid = true;
    const title = document.getElementById('sessionTitle').value.trim();
    const date = document.getElementById('sessionDate').value;
    const description = document.getElementById('sessionDescription').value.trim();
    
    // Validate title
    if (!title) {
        showFieldError('sessionTitle', 'Session title is required');
        isValid = false;
    } else if (title.length < 5) {
        showFieldError('sessionTitle', 'Title must be at least 5 characters long');
        isValid = false;
    }
    
    // Validate date
    if (!date) {
        showFieldError('sessionDate', 'Session date and time is required');
        isValid = false;
    } else {
        const selectedDate = new Date(date);
        const now = new Date();
        if (selectedDate <= now) {
            showFieldError('sessionDate', 'Session must be scheduled for a future date and time');
            isValid = false;
        }
    }
    
    // Validate description
    if (description && description.length < 10) {
        showFieldError('sessionDescription', 'Description must be at least 10 characters long');
        isValid = false;
    }
    
    return isValid;
}

function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    
    field.classList.add('is-invalid');
    field.parentNode.appendChild(errorDiv);
}

function clearValidationErrors() {
    // Remove all validation error messages
    document.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
    document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
}

function displayValidationErrors(errors) {
    clearValidationErrors();
    
    Object.keys(errors).forEach(fieldName => {
        const fieldId = `session${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)}`;
        const field = document.getElementById(fieldId);
        if (field) {
            showFieldError(fieldId, errors[fieldName].join(', '));
        }
    });
}

// Utility function for AJAX requests
function makeRequest(method, url, data, successMessage) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    const options = {
        method: method,
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    fetch(url, options)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(successMessage || data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}
