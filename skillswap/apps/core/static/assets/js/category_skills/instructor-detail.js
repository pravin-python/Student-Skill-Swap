document.addEventListener("DOMContentLoaded", function () {
  const coursesTab = document.querySelector("#courses");

  // Delegate click on pagination links
  coursesTab.addEventListener("click", function (e) {
    if (e.target.closest(".pagination a")) {
      e.preventDefault();
      const url = e.target.closest("a").getAttribute("href");

      fetch(url, {
        headers: { "x-requested-with": "XMLHttpRequest" }
      })
      .then(res => res.json())
      .then(data => {
        coursesTab.innerHTML = data.html; // replace grid + pagination
        window.scrollTo({ top: coursesTab.offsetTop - 100, behavior: "smooth" });
      });
    }
  });
});

