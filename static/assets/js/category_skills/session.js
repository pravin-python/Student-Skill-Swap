// Session management functions
function startSession(sessionId) {
    if (confirm('Start this session? This will mark it as active.')) {
        makeRequest('POST', `/courses/start_session/${sessionId}/`, null, 'Session started successfully!');
    }
}

function completeSession(sessionId) {
    if (confirm('Mark this session as completed?')) {
        makeRequest('POST', `/courses/complete_session/${sessionId}/`, null, 'Session marked as completed!');
    }
}

function openSessionCancellationModal(sessionId) {
    document.getElementById('cancellationSessionId').value = sessionId;
    document.getElementById('sessionCancellationForm').reset();
    
    const modal = new bootstrap.Modal(document.getElementById('sessionCancellationModal'));
    modal.show();
}

function submitSessionCancellation() {
    const form = document.getElementById('sessionCancellationForm');
    const formData = new FormData(form);
    
    if (!formData.get('reason').trim()) {
        alert('Please provide a reason for cancelling this session.');
        return;
    }
    
    const sessionId = formData.get('session_id');
    
    // Send cancellation request
    fetch(`/courses/cancel_session/${sessionId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Session cancelled successfully.');
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
    const modal = bootstrap.Modal.getInstance(document.getElementById('sessionCancellationModal'));
    modal.hide();
}

function deleteSession(sessionId) {
    if (confirm('Delete this session permanently?')) {
        makeRequest('POST', `/courses/delete_session/${sessionId}/`, null, 'Session deleted.');
    }
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
