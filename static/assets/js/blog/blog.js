document.addEventListener("DOMContentLoaded", function() {

  // Code for switching the positions between featured blog and last featured blog
  const API_URL = "/api/blogs/";
  const blogsWrapper = document.querySelector("#blogsWrapper #blog-posts");
  const blogHero = document.querySelector("#blog-hero .blog-grid");
  const searchInput = document.getElementById("searchInput");
  const sortSelect = document.querySelector(".sort-dropdown select");
  const categoryFilters = document.querySelectorAll("input[name='category']");
  const infiniteSpinner = document.getElementById("infiniteSpinner");

  let blogsData = [];
  let nextPageUrl = API_URL;
  let isLoading = false;

  // Fetch blogs
  async function fetchBlogs(url = API_URL, append = false) {
    if (!url || isLoading) return;
    isLoading = true;
    infiniteSpinner.style.display = "block";

    try {
      const response = await fetch(url);
      const data = await response.json();

      if (!append) {
        blogsData = data.results || data;
        renderFeaturedBlogs();
        renderRecentBlogs(blogsData, false);
      } else {
        blogsData = [...blogsData, ...(data.results || data)];
        renderRecentBlogs(data.results || data, true);
      }

      nextPageUrl = data.next;
    } catch (error) {
      console.error("Error fetching blogs:", error);
      if (!append) {
        blogsWrapper.innerHTML =
          `<p class="text-danger">Failed to load blogs.</p>`;
      }
    } finally {
      infiniteSpinner.style.display = nextPageUrl ? "block" : "none";
      isLoading = false;
    }
  }

  // Featured blogs
  function renderFeaturedBlogs() {
    blogHero.innerHTML = "";
    const featured = blogsData.slice(0, 2);
    featured.forEach((blog) => {
      const imgUrl = blog.thumbnail_image || "/static/assets/img/default-blog.jpg";
      const blogHTML = `
        <article class="blog-item" data-aos="fade-up">
          <img src="${imgUrl}" alt="${blog.title}">
          <div class="blog-content">
            <div class="post-meta d-flex justify-content-between mb-2">
              <span class="date">${new Date(blog.created_at).toLocaleDateString()}</span>
              <span class="category">${blog.category.name || "Uncategorized"}</span>
            </div>
            <h2 class="post-title mb-2">
              <a href="/blog-details/${blog.id}">${blog.title}</a>
            </h2>
            <div class="mt-1">
              <i class="bi bi-person"></i>
              <a href="/courses/instructor/${blog.author.id}/">
                <span class="featured-author">${blog.author.username}</span>
              </a>
            </div>
          </div>
        </article>
      `;
      blogHero.insertAdjacentHTML("beforeend", blogHTML);
    });
  }

  // Recent blogs
  function renderRecentBlogs(blogs, append = false) {
    const grid = document.getElementById("recentBlogsGrid");
    if (!append) {
      grid.innerHTML = "";
    }

    if (!append && blogs.length === 0) {
      grid.innerHTML = `<p class="text-center">No blog posts found.</p>`;
      return;
    }

    blogs.forEach((blog) => {
      const imgUrl = blog.thumbnail_image || "/static/assets/img/default-blog.jpg";
      const blogHTML = `
        <div class="col-lg-6 col-xl-4">
          <article class="blog-card h-100 border rounded shadow-sm">
            <div class="post-img position-relative overflow-hidden rounded-top">
              <img src="${imgUrl}" class="img-fluid w-100" alt="${blog.title}">
              <div class="post-date-badge">
                <span>${new Date(blog.created_at).getDate()}</span>
                <small>${new Date(blog.created_at).toLocaleString("default", { month: "long" })}</small>
              </div>
            </div>
            <div class="post-meta d-flex align-items-center px-3 mt-3">
              <div class="d-flex align-items-center me-3">
                <i class="bi bi-person"></i>
                <a href="/courses/instructor/${blog.author.id}/">
                  <span class="ps-2 author-name">${blog.author.username}</span>
                </a>
              </div>
              <span class="text-muted">/</span>
              <div class="d-flex align-items-center ms-3">
                <i class="bi bi-folder2"></i>
                <span class="category">${blog.category.name || "Uncategorized"}</span>
              </div>
            </div>
            <div class="post-content p-3">
              <h3 class="post-title">
                <a href="/blog-details/${blog.id}">${blog.title}</a>
              </h3>
              <a href="blog-detais/${blog.id}/" class="readmore">
                <span>Read More</span><i class="bi bi-arrow-right"></i>
              </a>
            </div>
          </article>
        </div>
      `;
      grid.insertAdjacentHTML("beforeend", blogHTML);
    });
  }

  // Filtering
  function applyFilters() {
    const query = searchInput.value.toLowerCase();
    const selectedCategories = Array.from(categoryFilters)
      .filter((cb) => cb.checked && cb.value !== "all")
      .map((cb) => parseInt(cb.value));

    let filtered = blogsData.filter((blog) => {
      const matchesSearch = blog.title.toLowerCase().includes(query);
      const matchesCategory =
        selectedCategories.length === 0 ||
        selectedCategories.includes(blog.category?.id);
      return matchesSearch && matchesCategory;
    });

    renderRecentBlogs(filtered);
    // Auto-scroll to #courses-2 section
    const coursesSection = document.getElementById("courses-2");
    if (coursesSection) 
    {
        coursesSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  searchInput.addEventListener("input", applyFilters);

  categoryFilters.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      if (checkbox.value === "all") {
        if (checkbox.checked) {
          categoryFilters.forEach((cb) => {
            if (cb.value !== "all") cb.checked = false;
          });
        }
      } else {
        document.querySelector("input[value='all']").checked = false;
      }
      applyFilters();
    });
  });

  sortSelect.addEventListener("change", function () {
    let sorted = [...blogsData];
    if (this.value.includes("Newest")) {
      sorted.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    } else if (this.value.includes("Oldest")) {
      sorted.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    }
    renderRecentBlogs(sorted);
  });

  // Infinite Scroll with IntersectionObserver
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting && nextPageUrl && !isLoading) {
        fetchBlogs(nextPageUrl, true);
      }
    },
    { rootMargin: "200px" }
  );
  observer.observe(infiniteSpinner);

  // Init
  fetchBlogs();
});
