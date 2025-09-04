document.addEventListener("DOMContentLoaded", function () {
  const departmentsTab = document.querySelector("#curriculum");

  // Delegate click on pagination links
  departmentsTab.addEventListener("click", function (e) {
    if (e.target.closest(".pagination a")) {
      e.preventDefault();
      const url = e.target.closest("a").getAttribute("href");

      fetch(url, {
        headers: { "x-requested-with": "XMLHttpRequest" }
      })
      .then(res => res.json())
      .then(data => {
        departmentsTab.innerHTML = data.html; // replace grid + pagination
        window.scrollTo({ top: departmentsTab.offsetTop - 100, behavior: "smooth" });
      });
    }
  });
});

