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
