// Handle pagination clicks
document.addEventListener("click", function (e) {
  if (e.target.closest(".pagination a")) {
    e.preventDefault();
    let url = e.target.closest("a").getAttribute("href");
    fetchCourses(url);
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
      fetchCourses(url);
    }, 500);
  });
}

// Handle category filter change
document.addEventListener("change", function (e) {
  if (e.target.matches("input[data-category]")) {
    let allCategoryCheckbox = document.querySelector("input[data-category='all']");
    let specificCategoryCheckboxes = [...document.querySelectorAll("input[data-category]:not([data-category='all'])")];

    if (e.target.getAttribute("data-category") === "all") {
      specificCategoryCheckboxes.forEach(cb => cb.checked = false);
    } else {
      if (allCategoryCheckbox) allCategoryCheckbox.checked = false;
      let allSelected = specificCategoryCheckboxes.every(cb => cb.checked);
      if (allSelected) {
        allCategoryCheckbox.checked = true;
        specificCategoryCheckboxes.forEach(cb => cb.checked = false);
      }
    }
    fetchCourses();
  }
});

// Handle level filter change
document.addEventListener("change", function (e) {
  if (e.target.matches("input[data-level]")) {
    let allLevelsCheckbox = document.querySelector("input[data-level='all']");
    let specificLevelCheckboxes = [...document.querySelectorAll("input[data-level]:not([data-level='all'])")];

    if (e.target.getAttribute("data-level") === "all") {
      specificLevelCheckboxes.forEach(cb => cb.checked = false);
    } else {
      if (allLevelsCheckbox) allLevelsCheckbox.checked = false;
      let allSelected = specificLevelCheckboxes.every(cb => cb.checked);
      if (allSelected) {
        allLevelsCheckbox.checked = true;
        specificLevelCheckboxes.forEach(cb => cb.checked = false);
      }
    }
    fetchCourses();
  }
});

// ✅ Core function: fetch courses
function fetchCourses(url = "?page=1") {
  let query = document.getElementById("searchInput")?.value || "";

  // collect selected categories
  let selectedCategories = [...document.querySelectorAll("input[data-category]:checked")]
    .map(cb => cb.getAttribute("data-category"));

  // collect selected levels
  let selectedLevels = [...document.querySelectorAll("input[data-level]:checked")]
    .map(cb => cb.getAttribute("data-level"));

  let params = new URLSearchParams();

  if (query) params.append("q", query);

  if (selectedCategories.length > 0) {
    selectedCategories.forEach(c => params.append("categories[]", c));
  }

  if (selectedLevels.length > 0) {
    selectedLevels.forEach(l => params.append("levels[]", l));
  }

  // Preserve page number
  if (url.includes("page=")) {
    params.set("page", new URL(url, window.location.origin).searchParams.get("page"));
  }

  // ✅ Force AJAX mode
  params.set("ajax", "1");

  fetch("?" + params.toString())
    .then(response => response.json())
    .then(data => {
      document.getElementById("coursesWrapper").innerHTML = data.html;

      // ✅ Clean URL (remove ajax=1 from history)
      params.delete("ajax");
      window.history.pushState({}, "", "?" + params.toString());

      window.scrollTo({ top: 0, behavior: "smooth" });
    })
    .catch(err => console.error("Error fetching courses:", err));
}

// ✅ Restore filter state on page load
(function restoreFiltersFromURL() {
  let params = new URLSearchParams(window.location.search);

  // Restore search input
  let q = params.get("q");
  if (q && searchInput) {
    searchInput.value = q;
  }

  // Restore selected categories
  let selectedCategories = params.getAll("categories[]");
  if (selectedCategories.length > 0) {
    document.querySelectorAll("input[data-category]").forEach(cb => {
      cb.checked = selectedCategories.includes(cb.getAttribute("data-category"));
    });
  }

  // Restore selected levels
  let selectedLevels = params.getAll("levels[]");
  if (selectedLevels.length > 0) {
    document.querySelectorAll("input[data-level]").forEach(cb => {
      cb.checked = selectedLevels.includes(cb.getAttribute("data-level"));
    });
  }
})();
