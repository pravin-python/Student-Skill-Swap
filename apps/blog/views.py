from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog , BlogSection , BlogImages
from apps.accounts.views import login_required_custom
from apps.accounts.models import User
from apps.category_skills.models import SkillsCategory
from django.contrib import messages
from django.http import JsonResponse

def BlogView(request):
    blogs = Blog.objects.filter(is_published=True).select_related("author")

    custom_user = request.session.get("user_id")

    # Excludes the blogs from the current logged-in user
    if custom_user:
        blogs = blogs.exclude(author=custom_user)

    categories = SkillsCategory.objects.all().order_by("name")

    return render(request, "blog/blog.html", {"blogs": blogs, "categories": categories})

def BlogDetailView(request, pk):
    blog = get_object_or_404(
        Blog.objects.select_related("author", "category").prefetch_related("sections", "images"),
        pk=pk,
        is_published=True
    )

    # Fetch ordered sections (each has its own `images` field)
    sections = blog.sections.all().order_by("order")

    # Pick blog's base image (from BlogImages model)
    base_image = blog.images.filter(base=True).first()

    return render(request, "blog/blog-details.html", {
        "blog": blog,
        "sections": sections,
        "base_image": base_image,   # available in template
    })


@login_required_custom
def BlogProfileView(request):
    user_id = request.session.get("user_id")
    user = get_object_or_404(User, id=user_id)

    user_blogs = Blog.objects.filter(author=user).prefetch_related("images").order_by("-created_at")  # user's blogs

    for blog in user_blogs:
        blog.thumbnail_image = blog.images.filter(thumbnail=True).first()

    context = {
        "custom_user": user,
        "user_blogs": user_blogs,
    }
    return render(request, "blog/blogs_profile.html", context)

@login_required_custom
def AddBlogView(request):
    user_id = request.session.get("user_id")    
    user = get_object_or_404(User, id=user_id)
    categories = SkillsCategory.objects.all()

    if request.method == "POST":
        try:
            title = request.POST.get("title")
            category_id = request.POST.get("category")
            intro = request.POST.get("intro")
            category = get_object_or_404(SkillsCategory, id=category_id) if category_id else None

            blog = Blog.objects.create(author=user, title=title, category=category, intro=intro)

            # --- Handle intro images ---
            files = request.FILES.getlist("intro_images_files[]")
            roles_list = request.POST.getlist("intro_images_roles[]")
            images_data = []
            for idx, file in enumerate(files):
                roles = roles_list[idx].split(",") if idx < len(roles_list) else []
                img = BlogImages.objects.create(
                    blog=blog,
                    image=file,
                    thumbnail="thumbnail" in roles,
                    base="base" in roles,
                    small="small" in roles,
                )
                images_data.append({
                    "id": img.id,
                    "url": img.image.url,
                    "roles": roles,
                })

            # --- Handle sections ---
            # --- Handle sections ---
            section_titles = request.POST.getlist("section_title[]")
            section_contents = request.POST.getlist("section_content[]")
            section_orders = request.POST.getlist("section_order[]")
            section_files = request.FILES.getlist("section_images[]")

            sections_data = []
            for idx, title in enumerate(section_titles):
                if not title and not (idx < len(section_contents) and section_contents[idx]):
                    continue

                sec = BlogSection.objects.create(
                    blog=blog,
                    title=title,
                    content=section_contents[idx] if idx < len(section_contents) else "",
                    order=section_orders[idx] if idx < len(section_orders) else 0,
                )

                if idx < len(section_files):
                    section_file = section_files[idx]
                    sec.images = section_file   
                    sec.save()
                    image_data = {"id": sec.id, "url": sec.images.url}
                else:
                    image_data = None

                sections_data.append({
                    "id": sec.id,
                    "title": sec.title,
                    "content": sec.content,
                    "order": sec.order,
                    "image": image_data,
                })

            return JsonResponse({
                "success": True,
                "message": "Your blog has been published successfully!",
                "blog_id": blog.id,
                "blog_title" : blog.title,
                "blog_content" : blog.intro,
                "images": images_data,
                "sections": sections_data,
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return render(request, "blog/add_blog.html", {"custom_user": user, "categories": categories})

@login_required_custom
def BlogEditView(request, pk):
    user_id = request.session.get("user_id")
    user = get_object_or_404(User, id=user_id)
    blog = get_object_or_404(
        Blog.objects.prefetch_related("sections", "images"),
        pk=pk,
        author=user,
    )
    categories = SkillsCategory.objects.all()

    if request.method == "POST":
        try:
            # Update basic blog info
            blog.title = request.POST.get("title")
            blog.category_id = request.POST.get("category")
            blog.intro = request.POST.get("intro")
            blog.save()

            # Handle existing blog images
            for img in blog.images.all():
                replace_file = request.FILES.get(f"replace_image_{img.id}")
                if replace_file:
                    img.image = replace_file
                role = request.POST.get(f"role_{img.id}") or "small"
                img.thumbnail = role == "thumbnail"
                img.base = role == "base"
                img.small = role == "small"
                img.save()

            # Handle new blog images
            new_images = request.FILES.getlist("images[]")
            new_roles = request.POST.getlist("image_role[]")
            for f, role in zip(new_images, new_roles):
                BlogImages.objects.create(
                    blog=blog,
                    image=f,
                    base=(role == "base"),
                    thumbnail=(role == "thumbnail"),
                    small=(role == "small"),
                )

            # Handle sections
            section_ids = request.POST.getlist("section_id[]")
            section_titles = request.POST.getlist("section_title[]")
            section_contents = request.POST.getlist("section_content[]")
            section_orders = request.POST.getlist("section_order[]")

            existing_sections = {str(s.id): s for s in blog.sections.all()}

            for idx, title in enumerate(section_titles):
                sec_id = section_ids[idx] if idx < len(section_ids) else None
                img_field = request.FILES.get(f"section_image_{sec_id}") if sec_id else None

                if sec_id and sec_id in existing_sections:
                    # Update existing section
                    sec = existing_sections[sec_id]
                    sec.title = title
                    sec.content = section_contents[idx]
                    sec.order = int(section_orders[idx]) if section_orders[idx] else 0
                    if img_field:
                        sec.images = img_field
                    sec.save()
                else:
                    # Create new section
                    BlogSection.objects.create(
                        blog=blog,
                        title=title,
                        content=section_contents[idx],
                        images=img_field,
                        order=int(section_orders[idx]) if section_orders[idx] else 0,
                    )

            # Delete sections removed in the form
            to_delete_ids = set(existing_sections.keys()) - set(section_ids)
            BlogSection.objects.filter(id__in=to_delete_ids).delete()

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True,
                    "message": "Blog updated successfully!",
                    "blog_id": blog.id,
                })

            messages.success(request, "Blog updated successfully!")
            return redirect("blog:blog-profile-view")

        except Exception as e:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": str(e)}, status=400)
            messages.error(request, f"Update failed: {e}")

    return render(
        request,
        "blog/edit_blog.html",
        {"blog": blog, "categories": categories},
    )


