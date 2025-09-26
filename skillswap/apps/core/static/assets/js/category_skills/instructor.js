// Handle pagination clicks
document.addEventListener("click", function (e) {
  if (e.target.closest(".pagination a")) {
    e.preventDefault();
    let url = e.target.closest("a").getAttribute("href");
    fetchInstructors(url);
  }
});

// Handle search input with debounce
let searchTimeout;
let searchInput = document.getElementById("searchInput");
if (searchInput) {
  searchInput.addEventListener("input", function (e) {
    clearTimeout(searchTimeout);
    let query = e.target.value;
    let url = "?q=" + encodeURIComponent(query);
    searchTimeout = setTimeout(() => {
      fetchInstructors(url);
    }, 500);
  });
}

// Handle category (department) filter change
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
    fetchInstructors();
  }
});

// ✅ Core fetch function
function fetchInstructors(url = "?page=1") {
  let query = document.getElementById("searchInput")?.value || "";

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

  // ✅ Force AJAX mode
  params.set("ajax", "1");

  fetch("?" + params.toString())
    .then(response => response.json())
    .then(data => {
      document.getElementById("instructorsWrapper").innerHTML = data.html;

      // ✅ Clean URL (remove ajax=1 from history)
      params.delete("ajax");
      window.history.pushState({}, "", "?" + params.toString());

      window.scrollTo({ top: 0, behavior: "smooth" });
    })
    .catch(err => console.error("Error fetching instructors:", err));
}

// ✅ Restore filter state on page load
(function restoreFiltersFromURL() {
  let params = new URLSearchParams(window.location.search);

  // Restore search box
  let q = params.get("q");
  if (q && searchInput) {
    searchInput.value = q;
  }

  // Restore department filters
  let selectedCategories = params.getAll("categories[]");
  if (selectedCategories.length > 0) {
    document.querySelectorAll("input[data-category]").forEach(cb => {
      if (selectedCategories.includes(cb.getAttribute("data-category"))) {
        cb.checked = true;
      } else {
        cb.checked = false;
      }
    });
  }
})();
