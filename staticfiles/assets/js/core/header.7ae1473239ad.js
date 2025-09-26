document.addEventListener("DOMContentLoaded", function () {
  const body = document.body;
  const themeToggle = document.getElementById("theme-toggle");
  const moonIcon = themeToggle.querySelector(".bi-moon-stars-fill");
  const sunIcon = themeToggle.querySelector(".bi-sun-fill");

  // Load saved theme or default to light
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    body.classList.add("dark-theme");
    moonIcon.classList.add("d-none");
    sunIcon.classList.remove("d-none");
  } else {
    body.classList.remove("dark-theme");
    moonIcon.classList.remove("d-none");
    sunIcon.classList.add("d-none");
  }

  // Toggle Theme on Click
  themeToggle.addEventListener("click", function () {
    body.classList.toggle("dark-theme");
    const darkMode = body.classList.contains("dark-theme");

    // Toggle icons
    moonIcon.classList.toggle("d-none", darkMode);
    sunIcon.classList.toggle("d-none", !darkMode);

    // Save preference
    localStorage.setItem("theme", darkMode ? "dark" : "light");
  });
});
