function addSkill(skillId) {
    console.log('Adding skill with ID:', skillId);
    
    // Get CSRF token from the form
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log('CSRF Token found:', csrfToken ? 'Yes' : 'No');
    
    if (!csrfToken) {
        alert('CSRF token not found. Please refresh the page and try again.');
        return;
    }
    
    const url = `/courses/add_skill/${skillId}/`;
    console.log('Making request to:', url);
    
    fetch(url, {    
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.success) {
            // Show success message
            alert(data.message);
            // Reload the page to update the skills
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding the skill. Please try again.');
    });
}

function removeSkill(skillId) {
    if (confirm('Are you sure you want to remove this skill from your profile?')) {
        console.log('Removing skill with ID:', skillId);
        
        // Get CSRF token from the form
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        console.log('CSRF Token found:', csrfToken ? 'Yes' : 'No');
        
        if (!csrfToken) {
            alert('CSRF token not found. Please refresh the page and try again.');
            return;
        }
        
        const url = `/courses/remove_skill/${skillId}/`;
        console.log('Making request to:', url);
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            if (data.success) {
                // Show success message
                alert(data.message);
                // Reload the page to update the skills
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while removing the skill. Please try again.');
        });
    }
}