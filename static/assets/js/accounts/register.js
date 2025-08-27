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