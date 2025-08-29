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
      // If "All Categories" clicked → uncheck others
      specificCategoryCheckboxes.forEach(cb => cb.checked = false);
    } else {
      // If any specific clicked → uncheck "All Categories"
      if (allCategoryCheckbox) allCategoryCheckbox.checked = false;

      // Check if ALL specific categories are selected
      let allSelected = specificCategoryCheckboxes.every(cb => cb.checked);
      
      if (allSelected) {
        // Reset → only "All Categories" checked
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

    fetchCourses();
  }
});


// Fetch courses with filters
function fetchCourses(url = "?page=1") {
  let query = document.getElementById("searchInput").value;

  // collect selected categories
  let selectedCategories = [...document.querySelectorAll("input[data-category]:checked")]
    .map(cb => cb.getAttribute("data-category"));

  // collect selected level courses 
  let selectedLevels = [...document.querySelectorAll("input[data-level]:checked")]
    .map(cb => cb.getAttribute("data-level"));

  let params = new URLSearchParams();

  if (query) params.append("q", query);

  if (selectedCategories.length > 0) {
    selectedCategories.forEach(c => params.append("categories[]", c));
  }

  if (selectedLevels.length > 0) {
    selectedLevels.forEach(l => params.append("levels[]", l))
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
      document.getElementById("coursesWrapper").innerHTML = data.html;
      window.history.pushState({}, "", "?" + params.toString());
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
}




