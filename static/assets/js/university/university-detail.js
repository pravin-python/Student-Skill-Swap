document.addEventListener("DOMContentLoaded", function () {
  function handlePagination(wrapperId, sectionName) {
    const wrapper = document.querySelector(wrapperId);
    if (!wrapper) return;

    wrapper.addEventListener("click", function (e) {
      const link = e.target.closest(".pagination a");
      if (link) {
        e.preventDefault();
        let url = new URL(link.href, window.location.origin);
        url.searchParams.set("section", sectionName); // add section to query

        fetch(url, {
          headers: { "x-requested-with": "XMLHttpRequest" }
        })
          .then(res => res.json())
          .then(data => {
            console.log()
            wrapper.innerHTML = data.html; // replace only this section
            window.scrollTo({ top: wrapper.offsetTop - 100, behavior: "smooth" });
          });
      }
    });
  }

  // Attach handlers for both sections
  handlePagination("#curriculum", "departments");
  handlePagination("#instructorsWrapper", "instructors");
});
