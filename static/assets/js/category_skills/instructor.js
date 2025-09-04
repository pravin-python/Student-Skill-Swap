// Handle pagination clicks
document.addEventListener("click", function (e) {
  if (e.target.closest(".pagination a")) {
    e.preventDefault();
    let url = e.target.closest("a").getAttribute("href");
    fetchCourses(url);
  }
});

// Handle search input
let searchtimeout;
document.getElementById("searchInput").addEventListener("input", function (e) {
  clearTimeout(searchtimeout);
  let query = e.target.value;
  let url = "?q=" + encodeURIComponent(query);
  searchtimeout = setTimeout(() => {
    fetchCourses(url);
  }, 500);
});

// Handle category filter change
document.addEventListener("change", function (e) {
  if (e.target.matches("input[data-category]")) {
    let allCategoryCheckbox = document.querySelector("input[data-category='all']");
    let specificCategoryCheckboxes = [...document.querySelectorAll("input[data-category]:not([data-category='all'])")];

    if (e.target.getAttribute("data-category") === "all") {
      // If "All" clicked → uncheck others
      specificCategoryCheckboxes.forEach(cb => cb.checked = false);
    } else {
      if (allCategoryCheckbox) allCategoryCheckbox.checked = false;

      // If all specific are selected → reset to "All"
      let allSelected = specificCategoryCheckboxes.every(cb => cb.checked);
      if (allSelected) {
        allCategoryCheckbox.checked = true;
        specificCategoryCheckboxes.forEach(cb => cb.checked = false);
      }
    }

    fetchCourses();
  }
});

// Fetch instructors
function fetchCourses(url = "?page=1") {
  let query = document.getElementById("searchInput").value;

  // Collect selected categories
  let selectedCategories = [...document.querySelectorAll("input[data-category]:checked")]
    .map(cb => cb.getAttribute("data-category"));

  let params = new URLSearchParams();

  if (query) params.append("q", query);

  if (selectedCategories.length > 0) {
    selectedCategories.forEach(c => params.append("categories[]", c));
  }

  // Preserve page param if exists
  if (url.includes("page=")) {
    params.set("page", new URL(url, window.location.origin).searchParams.get("page"));
  }

  fetch("?" + params.toString(), {
    headers: { "X-Requested-With": "XMLHttpRequest" }
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("instructorsWrapper").innerHTML = data.html;
      window.history.pushState({}, "", "?" + params.toString());
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
}
