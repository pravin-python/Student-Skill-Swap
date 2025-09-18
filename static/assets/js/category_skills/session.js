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
    
    const modal = bootstrap.Modal.getInstance(document.getElementById('sessionCancellationModal'));
    modal.hide();
}

function deleteSession(sessionId) {
    if (confirm('Delete this session permanently?')) {
        makeRequest('POST', `/courses/delete_session/${sessionId}/`, null, 'Session deleted.');
    }
}

function makeRequest(method, url, data, successMessage) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    const options = {
        method: method, 
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        }
    };
    
    if (data) options.body = JSON.stringify(data);
    
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

document.addEventListener("DOMContentLoaded", function () {

    // ======= Feedback Modal Handling =======
    const feedbackModal = document.getElementById('feedbackModal');
    const feedbackForm = document.getElementById('feedbackForm');

    if (feedbackModal) {
        feedbackModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const sessionId = button.getAttribute('data-session-id');
            document.getElementById('feedbackSessionId').value = sessionId;

            // Set role label
            const roleSpan = document.getElementById('feedbackRole');
            if (button.closest('#teaching-container')) {
                roleSpan.textContent = "Learner"; // Teacher is giving feedback
            } else {
                roleSpan.textContent = "Teacher"; // Learner is giving feedback
            }
        });

        feedbackForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(feedbackForm);
            const sessionId = formData.get('session_id');

            fetch(`/sessions/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);

                    // Update the feedback button
                    const buttonContainer = document.querySelector(`#teaching-container [data-session-id="${sessionId}"], #learning-container [data-session-id="${sessionId}"]`);
                    if (buttonContainer) {
                        const btnGroup = buttonContainer.closest('.btn-group');
                        if (btnGroup) {
                            btnGroup.innerHTML = data.button_html;
                        }
                    }

                    // Close modal
                    const modalInstance = bootstrap.Modal.getInstance(feedbackModal);
                    modalInstance.hide();
                } else {
                    alert(data.error || data.message);
                }
            })
            .catch(err => {
                console.error(err);
                alert('Error submitting feedback.');
            });
        });
    }

    // ======= Pagination Handling =======
    function handlePagination(wrapperId, sectionName) {
        const wrapper = document.querySelector(wrapperId);
        if (!wrapper) return;

        wrapper.addEventListener("click", function (e) {
            const link = e.target.closest(".pagination a");
            if (link) {
                e.preventDefault();
                let url = new URL(link.href, window.location.origin);
                url.searchParams.set("section", sectionName);

                fetch(url, {
                    headers: { "x-requested-with": "XMLHttpRequest" }
                })
                .then(res => res.json())
                .then(data => {
                    wrapper.innerHTML = data.html;
                    window.scrollTo({ top: wrapper.offsetTop - 100, behavior: "smooth" });
                });
            }
        });
    }

    handlePagination("#teaching-container", "teaching");
    handlePagination("#learning-container", "learning");
});
