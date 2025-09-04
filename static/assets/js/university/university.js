// Handle pagination clicks
document.addEventListener("click", function (e) {
  if (e.target.closest(".pagination a")) {
    e.preventDefault();
    let url = e.target.closest("a").getAttribute("href");
    fetchUniversities(url);
  }
});

// Handle search input
let searchtimeout;
document.getElementById("searchInput").addEventListener("input", function (e) {
  clearTimeout(searchtimeout);
  let query = e.target.value;
  let url = "?q=" + encodeURIComponent(query);
  searchtimeout = setTimeout(() => {
    fetchUniversities(url);
  }, 500);
});

// Handle category filter change
document.addEventListener("change", function (e) {
  if (e.target.matches("input[data-category]")) {
    let allCategoryCheckbox = document.querySelector("input[data-category='all']");
    let specificCategoryCheckboxes = [...document.querySelectorAll("input[data-category]:not([data-category='all'])")];

    if (e.target.value === "all") {
      // If "All Departments" clicked → uncheck others
      specificCategoryCheckboxes.forEach(cb => cb.checked = false);
    } else {
      // If any specific clicked → uncheck "All Departments"
      if (allCategoryCheckbox) allCategoryCheckbox.checked = false;

      // Check if ALL specific departments are selected
      let allSelected = specificCategoryCheckboxes.every(cb => cb.checked);

      if (allSelected) {
        // Reset → only "All Departments" checked
        allCategoryCheckbox.checked = true;
        specificCategoryCheckboxes.forEach(cb => cb.checked = false);
      }
    }

    fetchUniversities();
  }
});

// Handle level filter change
document.addEventListener("change", function (e) {
  if (e.target.matches("input[data-level]")) {
    let allLevelsCheckbox = document.querySelector("input[data-level='all']");
    let specificLevelCheckboxes = [...document.querySelectorAll("input[data-level]:not([data-level='all'])")];

    if (e.target.value === "all") {
      // If "All Levels" clicked → uncheck others
      specificLevelCheckboxes.forEach(cb => cb.checked = false);
    } else {
      // If any specific clicked → uncheck "All Levels"
      if (allLevelsCheckbox) allLevelsCheckbox.checked = false;

      // Check if ALL specific levels are selected
      let allSelected = specificLevelCheckboxes.every(cb => cb.checked);

      if (allSelected) {
        // Reset → only "All Levels" checked
        allLevelsCheckbox.checked = true;
        specificLevelCheckboxes.forEach(cb => cb.checked = false);
      }
    }

    fetchUniversities();
  }
});

// Fetch universities with filters
function fetchUniversities(url = "?page=1") {
  let query = document.getElementById("searchInput").value;

  // collect selected categories (departments)
  let selectedCategories = [...document.querySelectorAll("input[data-category]:checked")]
    .map(cb => cb.value);

  // collect selected levels
  let selectedLevels = [...document.querySelectorAll("input[data-level]:checked")]
    .map(cb => cb.value);

  let params = new URLSearchParams();

  if (query) params.append("q", query);

  if (selectedCategories.length > 0) {
    selectedCategories.forEach(c => params.append("categories[]", c));
  }

  if (selectedLevels.length > 0) {
    selectedLevels.forEach(l => params.append("levels[]", l));
  }

  // if url already has ?page= keep page number
  if (url.includes("page=")) {
    params.set("page", new URL(url, window.location.origin).searchParams.get("page"));
  }

  fetch("?" + params.toString(), {
    headers: { "X-Requested-With": "XMLHttpRequest" }
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("universitiesWrapper").innerHTML = data.html;
      window.history.pushState({}, "", "?" + params.toString());
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
}
