document.addEventListener("DOMContentLoaded", function() {
const container = document.getElementById("sections-container");
    const addBtn = document.getElementById("add-section");

    // Function to initialize CKEditor on all .rich-editor textareas
    function initEditors() {
        document.querySelectorAll(".rich-editor").forEach((textarea) => {
            if (!textarea.hasAttribute("data-ckeditor-initialized")) {
                CKEDITOR.replace(textarea, {
                    height: 150
                });
                textarea.setAttribute("data-ckeditor-initialized", "true");
            }
        });
    }

    // Adding new sections everytime the user clicks on add section
    addBtn.addEventListener("click", function() {
        const newSection = document.createElement("div");
        newSection.classList.add("card", "border", "mb-3", "section-item");
        newSection.innerHTML = `
            <div class="card-body">
                <div class="mb-2">
                    <label class="form-label">Section Title</label>
                    <input type="text" name="section_title[]" class="form-control" placeholder="Enter section title">
                </div>
                <div class="mb-2">
                    <label class="form-label">Content</label>
                    <textarea name="section_content[]" class="form-control rich-editor" rows="4" placeholder="Write section content..."></textarea>
                </div>
                <div class="mb-2">
                    <label class="form-label">Order</label>
                    <input type="number" name="section_order[]" class="form-control" value="0" min="0">
                </div>
                <button type="button" class="btn btn-sm btn-outline-danger remove-section">
                    <i class="bi bi-trash"></i> Remove Section
                </button>
            </div>
        `;
        container.appendChild(newSection);

        // Initialize CKEditor for the new textarea everytime the add section appears
        initEditors();
    });

    // Removing section everytimes the user click on removes section 
    container.addEventListener("click", function(e) {
        if (e.target.closest(".remove-section")) {
            const section = e.target.closest(".section-item");
            const textarea = section.querySelector("textarea");

            // Destroy CKEditor instance before removing
            if (textarea && textarea.id && CKEDITOR.instances[textarea.id]) {
                CKEDITOR.instances[textarea.id].destroy(true);
            }

            section.remove();
        }
    });

    // Initialize CKEditor for intro and first section on page load
    CKEDITOR.replace("intro-editor", { height: 200 });
    initEditors();
});
