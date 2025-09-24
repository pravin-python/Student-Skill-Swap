document.addEventListener("DOMContentLoaded", function () {
  const skillsContainer = document.getElementById("skillsContainer");
  renderInstructors("/api/instructors/", "#instructorsContainer");
  const apiUrl = "/api/courses/";

  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      const skills = data.skills;

      if (skills.length === 0) {
        skillsContainer.innerHTML = `
          <div class="col-12">
            <div class="text-center py-5">
              <h4>No skills available at the moment</h4>
              <p>Please check back later for new courses and skills.</p>
            </div>
          </div>`;
        return;
      }

      let skillsHtml = "";

      skills.forEach(skill => {
        skillsHtml += `
          <div class="col-lg-4 col-md-6 course-item pb-4"
               data-category="${skill.category.id}"
               data-skill-name="${skill.name.toLowerCase()}"
               data-category-name="${skill.category.name.toLowerCase()}">
            <div class="course-card">
              <div class="course-image">
                <img src="${skill.image ? skill.image : '/static/assets/img/education/courses-3.webp'}"
                     alt="${skill.name}" class="img-fluid">
                <div class="course-badge">${skill.category.name}</div>
              </div>
              <div class="course-content">
                <div class="course-meta">
                  <span class="category">${skill.category.name}</span>
                  <span class="level">${skill.level_display}</span>
                </div>
                <h3><a href ="courses/course_details/${skill.student.username}/${skill.slug}/">${skill.name}</a></h3>
                <p>${skill.description ? skill.description.split(" ").slice(0,20).join(" ") + "..." : ""}</p>
                <div class="course-stats">
                  <div class="stat"><i class="bi bi-calendar"></i>
                    <span>Added ${new Date(skill.created_at).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}</span>
                  </div>
                  <div class="stat"><i class="bi bi-people"></i>
                    <span>Learn this skill</span>
                  </div>
                </div>
                ${skill.student ? `
                <p class="teacher-name mt-3 p-2 bg-light rounded d-inline-block shadow-sm">
                  <i class="bi bi-person text-primary"></i>
                  <strong>Student: <a href = "/courses/instructor/${skill.student.username}/"> ${skill.student.first_name} ${skill.student.last_name} </a></strong>
                </p>` : ""}
                <a href="/courses/course_details/${skill.student.username}/${skill.slug}" class="btn-course">Course Details -> </a>
              </div>
            </div>
          </div>
        `;
      });

      skillsContainer.innerHTML = skillsHtml;
    })
    .catch(error => {
      console.error("Error fetching skills:", error);
      skillsContainer.innerHTML = `
        <div class="col-12">
          <div class="text-center py-5">
            <h4>Error loading skills</h4>
            <p>Please try again later.</p>
          </div>
        </div>`;
    });
});


// Function to create a single instructor card
function createInstructorCard(instructor) {
    // Create main column div
    const colDiv = document.createElement("div");
    colDiv.className = "col-xl-3 col-lg-4 col-md-6";
    colDiv.setAttribute("data-aos", "fade-up");
    colDiv.setAttribute("data-aos-delay", "200");

    // Card container
    const cardDiv = document.createElement("div");
    cardDiv.className = "instructor-card";

    // Image section
    const imageDiv = document.createElement("div");
    imageDiv.className = "instructor-image";

    const img = document.createElement("img");
    img.className = "img-fluid";
    img.alt = `${instructor.user.first_name}`;

    // Use profile pic or default
    img.src = instructor.user.profile_pic || "/static/assets/img/default-avatar.webp";

    // Overlay content
    const overlayDiv = document.createElement("div");
    overlayDiv.className = "overlay-content";

    // Rating stars
    const ratingDiv = document.createElement("div");
    ratingDiv.className = "rating-stars";
    ratingDiv.innerHTML = `
        <i class="bi bi-star-fill"></i>
        <i class="bi bi-star-fill"></i>
        <i class="bi bi-star-fill"></i>
        <i class="bi bi-star-fill"></i>
        <i class="bi bi-star-half"></i>
        <span>4.8</span>
    `;

    // Skills count
    const courseDiv = document.createElement("div");
    courseDiv.className = "course-count";
    courseDiv.innerHTML = `
        <i class="bi bi-award"></i>
        <span>${instructor.skills_count} Skills</span>
    `;

    overlayDiv.appendChild(ratingDiv);
    overlayDiv.appendChild(courseDiv);
    imageDiv.appendChild(img);
    imageDiv.appendChild(overlayDiv);

    // Info section
    const infoDiv = document.createElement("div");
    infoDiv.className = "instructor-info";
    infoDiv.innerHTML = `
        <h5 class = "instructorname"><a href = "/courses/instructor/${instructor.user.username}/">${instructor.user.first_name} ${instructor.user.last_name}</a></h5>
        <p class="specialty">${instructor.user.department?.name || "Student"}</p>
        <p class="description">${truncateWords(instructor.user.bio || "A passionate student sharing knowledge and skills.", 15)}</p>
    `;

    // Skills list
    const skillsDiv = document.createElement("div");
    skillsDiv.className = "skills-list mb-3";
    skillsDiv.innerHTML = `<small class="text-muted">Skills:</small>`;
    const skillContainer = document.createElement("div");
    skillContainer.className = "d-flex flex-wrap gap-1 mt-1";

    instructor.skills.slice(0, 3).forEach(skill => {
        const span = document.createElement("span");
        span.className = "badge bg-primary";
        span.textContent = skill.name;
        skillContainer.appendChild(span);
    });

    if (instructor.skills_count > 3) {
        const moreSpan = document.createElement("span");
        moreSpan.className = "badge bg-secondary";
        moreSpan.textContent = `+${instructor.skills_count - 3} more`;
        skillContainer.appendChild(moreSpan);
    }

    skillsDiv.appendChild(skillContainer);
    infoDiv.appendChild(skillsDiv);

    // Stats grid
    const statsDiv = document.createElement("div");
    statsDiv.className = "stats-grid";
    statsDiv.innerHTML = `
        <div class="stat">
            <span class="number">${instructor.skills_count}</span>
            <span class="label">Skills</span>
        </div>
        <div class="stat">
            <span class="number">${instructor.user.year}</span>
            <span class="label">Year</span>
        </div>
    `;
    infoDiv.appendChild(statsDiv);

    // Action buttons
    const actionDiv = document.createElement("div");
    actionDiv.className = "action-buttons";
    actionDiv.innerHTML = `
        <a href="/courses/instructor/${instructor.user.username}/" class="btn-view">View Profile</a>
        <div class="social-links">
            <a href="#"><i class="bi bi-envelope"></i></a>
            <a href="#"><i class="bi bi-person"></i></a>
        </div>
    `;
    infoDiv.appendChild(actionDiv);

    cardDiv.appendChild(imageDiv);
    cardDiv.appendChild(infoDiv);
    colDiv.appendChild(cardDiv);

    return colDiv;
}

// Helper function to truncate words
function truncateWords(text, num) {
    const words = text.split(" ");
    if (words.length <= num) return text;
    return words.slice(0, num).join(" ") + "...";
}

// Render instructors list from JSON API
// Render instructors list from JSON API
function renderInstructors(apiUrl, containerSelector) {
    const container = document.querySelector(containerSelector);

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            container.innerHTML = ""; // clear previous instructors

            if (data.instructors_data && data.instructors_data.length > 0) {
                data.instructors_data.forEach(instructor => {
                    const card = createInstructorCard(instructor);
                    container.appendChild(card); // directly append card to instructorsContainer
                });
            } else {
                container.innerHTML = `
                    <div class="col-12">
                        <div class="text-center py-5">
                            <h4>No instructors available</h4>
                            <p>No users have added skills to their profiles yet.</p>
                        </div>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error("Error fetching instructors:", error);
            container.innerHTML = `
                <div class="col-12">
                    <p class="text-danger text-center">Failed to load instructors.</p>
                </div>
            `;
        });
}




