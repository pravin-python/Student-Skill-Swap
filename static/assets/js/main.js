/**
* Template Name: Learner
* Template URL: https://bootstrapmade.com/learner-bootstrap-course-template/
* Updated: Jul 08 2025 with Bootstrap v5.3.7
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /*
   * Pricing Toggle
   */

  const pricingContainers = document.querySelectorAll('.pricing-toggle-container');

  pricingContainers.forEach(function(container) {
    const pricingSwitch = container.querySelector('.pricing-toggle input[type="checkbox"]');
    const monthlyText = container.querySelector('.monthly');
    const yearlyText = container.querySelector('.yearly');

    pricingSwitch.addEventListener('change', function() {
      const pricingItems = container.querySelectorAll('.pricing-item');

      if (this.checked) {
        monthlyText.classList.remove('active');
        yearlyText.classList.add('active');
        pricingItems.forEach(item => {
          item.classList.add('yearly-active');
        });
      } else {
        monthlyText.classList.add('active');
        yearlyText.classList.remove('active');
        pricingItems.forEach(item => {
          item.classList.remove('yearly-active');
        });
      }
    });
  });

})();

/* Populating fields into Register Pop up Modal  
 * 
 */
document.addEventListener("DOMContentLoaded", function () {
    // --- Populate form choices ---
    fetch("/api/get-choices/")
        .then(response => response.json())
        .then(data => {
            // Universities
            const uniSelect = document.getElementById("university_name");
            data.universities.forEach(u => {
                const opt = document.createElement("option");
                opt.value = u.id;
                opt.textContent = u.name;
                uniSelect.appendChild(opt);
            });

            // Departments
            const deptSelect = document.getElementById("department");
            data.departments.forEach(d => {
                const opt = document.createElement("option");
                opt.value = d.id;
                opt.textContent = d.name;
                deptSelect.appendChild(opt);
            });

            // Branches
            const branchSelect = document.getElementById("branch");
            data.branches.forEach(b => {
                const opt = document.createElement("option");
                opt.value = b.id;
                opt.textContent = b.name;
                branchSelect.appendChild(opt);
            });

            // Years
            const yearSelect = document.getElementById("year");
            data.years.forEach(([value, label]) => {
                const opt = document.createElement("option");
                opt.value = value;
                opt.textContent = label;
                yearSelect.appendChild(opt);
            });

            // Genders (radio buttons)
            const genderContainer = document.getElementById("gender");
            data.genders.forEach(([value, label]) => {
                const div = document.createElement("div");
                div.classList.add("form-check", "form-check-inline");

                const input = document.createElement("input");
                input.type = "radio";
                input.name = "gender";
                input.id = "gender_" + value;
                input.value = value;
                input.classList.add("form-check-input");

                const lab = document.createElement("label");
                lab.setAttribute("for", "gender_" + value);
                lab.classList.add("form-check-label");
                lab.textContent = label;

                div.appendChild(input);
                div.appendChild(lab);
                genderContainer.appendChild(div);
            });
        })
        .catch(error => console.error("Error loading form choices:", error));

    // --- Handle form submission (only once) ---
    document.getElementById("registerForm").addEventListener("submit", async function (e) {
        e.preventDefault();

        const form = e.target;
        const url = form.getAttribute("data-url");
        let isValid = true;
        
        form.querySelectorAll(".error-text").forEach(el => el.remove());
        form.querySelectorAll(".is-invalid").forEach(el => el.classList.remove("is-invalid"));

         // Helper to show error below input
        function showError(inputName, message) {
        let input = form.querySelector(`[name="${inputName}"]`);
        if (input) {
            input.classList.add("is-invalid"); // red border (Bootstrap)
            let error = document.createElement("small");
            error.className = "error-text text-danger d-block mt-1";
            error.innerText = message;
            if(input.type === "radio" || input.type === "checkbox") {
                let parentDiv = input.closest(".mb-3") || input.parentElement;
                parentDiv.appendChild(error);
            }
            else {
                input.classList.add("is-invalid");
                input.insertAdjacentElement("afterend", error);
            }
            
            isValid = false;
        }
    }

    // --- Grab values ---
        let username = form.username.value.trim();
        let first_name = form.first_name.value.trim();
        let last_name = form.last_name.value.trim();
        let gender = form.gender.value.trim();
        let email = form.personal_email.value.trim();
        let university = form.university_name.value;
        let department = form.department.value;
        let branch = form.branch.value;
        let year = form.year.value;
        let password = form.current_password.value.trim();
        let confirm_password = form.confirm_password.value.trim();

    // --- VALIDATIONS (frontend) ---
        if (!username) showError("username", "Username is required.");
        if (!first_name) {showError("first_name", "First name is required.");}
        else if (!/^[A-Za-z]+$/.test(first_name)) {showError("first_name", "First name must contain only alphabets.");}
        if (!last_name) showError("last_name", "Last name is required.");
        else if (!/^[A-Za-z]+$/.test(first_name)) {showError("last_name", "Last name must contain only alphabets.");}
        if (!gender) showError("gender","Please Select a gender.");
        if (!email) showError("personal_email", "Email is required.");
        else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) showError("personal_email", "Enter a valid email.");
        if (!university) showError("university_name", "Please select a university.");
        if (!department) showError("department", "Please select a department.");
        if (!branch) showError("branch", "Please select a branch.");
        if (!year) showError("year", "Please select a year.");
        if (!password) showError("current_password", "Password is required.");
        else if (password.length < 8) showError("current_password", "Password must be at least 8 characters long.");
        if (!confirm_password) showError("confirm_password","Confirm Password is required")
        if(password !== confirm_password) showError("confirm_password","Passwords Do Not Match.")

    // --- Stop if frontend validation failed ---
        if (!isValid) return;

    // --- If frontend validation passes, call backend via fetch ---
        try {
            let formData = new FormData(form);
            const response = await fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const data = await response.json();

            if (data.success) {
                // Close register modal and open login modal
                const registerModal = document.getElementById("openregisterModal");
                const loginModal = document.getElementById("openloginModal");

                if (registerModal) {
                    const bsModal = bootstrap.Modal.getInstance(registerModal);
                    bsModal.hide();
                }
                if (loginModal) {
                    const bsModal = new bootstrap.Modal(loginModal);
                    bsModal.show();
                }
            } else {
                // Show field errors
                if (data.errors) {
                    for (let field in data.errors) {
                        const input = form.querySelector(`[name=${field}]`);
                        if (input) {
                            input.insertAdjacentHTML(
                                "afterend",
                                `<span class="error-text text-danger">${data.errors[field]}</span>`
                            );
                        }
                    }
                } else {
                    alert("Error: " + (data.message || "Something went wrong"));
                }
            }
        } catch (err) {
            console.error("Request failed", err);
            alert("Something went wrong. Please try again.");
        }
    });
});

/*
* Script for login form field errors
*/
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();
        let form = e.target;

        // --- Clear previous errors ---
        document.getElementById("usernameError").innerText = "";
        document.getElementById("passwordError").innerText = "";

        let username = form.username.value.trim();
        let password = form.password.value.trim();
        let isValid = true;

        // --- Frontend validation ---
        if (!username) {
            document.getElementById("usernameError").innerText = "Username or Email is required.";
            isValid = false;
        }

        if (!password) {
            document.getElementById("passwordError").innerText = "Password is required.";
            isValid = false;
        }

        // ❌ Stop here if invalid
        if (!isValid) return;

        // ✅ Call backend only if frontend validation passed
        let data = new FormData(form);

        fetch(form.action, {
            method: "POST",
            headers: { "X-Requested-With": "XMLHttpRequest" },
            body: data
        })
            .then(res => res.json())
            .then(res => {
                console.log("Response from server:", res);

                if (res.success) {
                    window.location.href = "/"; // redirect to homepage
                } else {
                    // Show backend errors inline
                    if (res.errors.username) {
                        document.getElementById("usernameError").innerText = res.errors.username;
                    }
                    if (res.errors.password) {
                        document.getElementById("passwordError").innerText = res.errors.password;
                    }
                }
            })
            .catch(err => console.error(err));
    });
}


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

// Show message likes profile updated successfully 
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

