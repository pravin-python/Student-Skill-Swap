document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("sections-container");
    const addBtn = document.getElementById("add-section");
    const introInput = document.getElementById("intro-images");

        // ✅ Global Toast Function
    window.showToast = function (message, isError = false) {
        let toastContainer = document.getElementById("toast-container");
        if (!toastContainer) {
            toastContainer = document.createElement("div");
            toastContainer.id = "toast-container";
            toastContainer.style.position = "fixed";
            toastContainer.style.top = "1rem";
            toastContainer.style.right = "1rem";
            toastContainer.style.zIndex = "9999";
            document.body.appendChild(toastContainer);
        }

        const toast = document.createElement("div");
        toast.className = `toast align-items-center text-white ${isError ? "bg-danger" : "bg-success"} border-0 show mb-2`;
        toast.role = "alert";
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        toastContainer.appendChild(toast);

        setTimeout(() => { toast.remove(); }, 4000);
    };

    function initEditors() {
        if (!window.CKEDITOR) return;
        document.querySelectorAll(".rich-editor").forEach((textarea) => {
            if (!textarea.hasAttribute("data-ckeditor-initialized")) {
                if (!textarea.id) {
                    textarea.id = "editor-" + Date.now() + "-" + Math.floor(Math.random() * 1000);
                }
                try {
                    CKEDITOR.replace(textarea.id, { height: 150 });
                    textarea.setAttribute("data-ckeditor-initialized", "true");
                } catch (e) {
                    console.warn("CKEditor init failed", e);
                }
            }
        });
    }

    let introFiles = [];

    function attachIntroImagePreview(input) {
        const previewContainer = input.closest(".card-body")?.querySelector(".image-preview-container");
        if (!previewContainer) return;

        input.addEventListener("change", function () {
            Array.from(this.files).forEach((file) => {
                introFiles.push(file);
                const reader = new FileReader();
                reader.onload = function (e) {
                    const wrapper = document.createElement("div");
                    wrapper.classList.add("card", "p-2", "mb-2");
                    wrapper.fileRef = file;

                    wrapper.innerHTML = `
                        <div class="d-flex align-items-center">
                            <img src="${e.target.result}" alt="preview"
                                class="me-3 rounded"
                                style="width:80px;height:80px;object-fit:cover;">
                            <div>
                                <p class="mb-1 fw-bold">${file.name}</p>
                                <div class="form-check">
                                    <input class="form-check-input role-checkbox" type="checkbox" value="thumbnail">
                                    <label class="form-check-label">Thumbnail</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input role-checkbox" type="checkbox" value="base">
                                    <label class="form-check-label">Base</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input role-checkbox" type="checkbox" value="small">
                                    <label class="form-check-label">Small</label>
                                </div>
                            </div>
                        </div>
                    `;

                    const roleInput = document.createElement("input");
                    roleInput.type = "hidden";
                    roleInput.name = "intro_images_roles[]";
                    roleInput.value = "";
                    wrapper.appendChild(roleInput);

                    previewContainer.appendChild(wrapper);

                    const checkboxes = wrapper.querySelectorAll(".role-checkbox");
                    function updateRole() {
                        let roles = [];
                        checkboxes.forEach(cb => { if (cb.checked) roles.push(cb.value); });
                        roleInput.value = roles.join(",");
                    }
                    checkboxes.forEach(cb => cb.addEventListener("change", updateRole));
                };
                reader.readAsDataURL(file);
            });

            this.value = "";
        });
    }

    function attachSectionImagePreview(input) {
        const previewContainer = input.closest(".card-body")?.querySelector(".image-preview-container");
        if (!previewContainer) return;

        input.addEventListener("change", function () {
            previewContainer.innerHTML = "";
            Array.from(this.files).forEach((file) => {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const wrapper = document.createElement("div");
                    wrapper.classList.add("card", "p-2", "mb-2");
                    wrapper.innerHTML = `
                        <div class="d-flex align-items-center">
                            <img src="${e.target.result}" alt="preview" class="me-3 rounded" style="width:80px;height:80px;object-fit:cover;">
                            <p class="mb-0 fw-bold">${file.name}</p>
                        </div>
                    `;
                    previewContainer.appendChild(wrapper);
                };
                reader.readAsDataURL(file);
            });
        });
    }

    if (introInput) attachIntroImagePreview(introInput);
    document.querySelectorAll(".section-image-input").forEach(input => attachSectionImagePreview(input));

    addBtn.addEventListener("click", function () {
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
            <div class="mb-3">
                <label class="form-label fw-bold">Upload Section Images</label>
                <input type="file" class="form-control section-image-input" name="section_images[]" accept="image/*">
            </div>
            <div class="image-preview-container mb-4"></div>
            <div class="mb-2">
                <label class="form-label">Order</label>
                <input type="number" name="section_order[]" class="form-control" value="0" min="0">
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger remove-section">
                <i class="bi bi-trash"></i> Remove Section
            </button>
        </div>`;
        container.appendChild(newSection);
        initEditors();
        newSection.querySelectorAll(".section-image-input").forEach(input => attachSectionImagePreview(input));
    });

    container.addEventListener("click", function (e) {
        if (e.target.closest(".remove-section")) {
            const section = e.target.closest(".section-item");
            const textarea = section.querySelector("textarea");
            if (textarea && textarea.id && CKEDITOR.instances[textarea.id]) {
                CKEDITOR.instances[textarea.id].destroy(true);
            }
            section.remove();
        }
    });

function handleFormSubmit(targetForm) {
    if (!targetForm) return;
    targetForm.addEventListener("submit", function (e) {
        e.preventDefault();

        // Update CKEditor fields
        if (window.CKEDITOR && CKEDITOR.instances) {
            for (let instance in CKEDITOR.instances) {
                if (Object.prototype.hasOwnProperty.call(CKEDITOR.instances, instance)) {
                    try { CKEDITOR.instances[instance].updateElement(); } catch(_) {}
                }
            }
        }

        const formData = new FormData(targetForm);

        // Add intro image files and roles
        document.querySelectorAll(".image-preview-container .card").forEach((wrapper) => {
            const roleInput = wrapper.querySelector("input[name='intro_images_roles[]']");
            if (wrapper.fileRef) {
                formData.append("intro_images_files[]", wrapper.fileRef);
                formData.append("intro_images_roles[]", roleInput.value || "");
            }
        });

        // 🔎 Debug: Print FormData as JSON-like object
        const debugData = {};
        for (let [key, value] of formData.entries()) {
            debugData[key] = value instanceof File ? `[File: ${value.name}, ${value.size} bytes]` : value;
        }
        console.log("API Request Data:", JSON.stringify(debugData, null, 2));

        // ✅ Make the API request
        fetch(targetForm.action || window.location.href, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")?.value || "",
            },
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                showToast(data.message || "Saved successfully");
            } else {
                showToast(data.error || "Save failed", true);
            }
        })  
        .catch(err => {
            console.error("Request failed:", err);
            showToast("Something went wrong while saving the blog.", true);
        });
    });
}


    handleFormSubmit(document.getElementById("add-blog-form"));
    handleFormSubmit(document.getElementById("edit-blog-form"));

    if (document.getElementById("intro-editor") && window.CKEDITOR) {
        try { CKEDITOR.replace("intro-editor", { height: 200 }); } catch(_) {}
    }
    initEditors();
});
