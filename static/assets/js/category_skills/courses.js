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
    fetchCourses();
  }
});

// Fetch courses with filters
function fetchCourses(url = "?page=1") {
  let query = document.getElementById("searchInput").value;

  // collect selected categories
  let selectedCategories = [...document.querySelectorAll("input[data-category]:checked")]
    .map(cb => cb.getAttribute("data-category"));

  let params = new URLSearchParams();

  if (query) params.append("q", query);
  if (selectedCategories.length > 0) {
    selectedCategories.forEach(c => params.append("categories[]", c));
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


