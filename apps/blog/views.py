from django.shortcuts import render, get_object_or_404 , redirect
from .models import Blog , BlogSection
from apps.accounts.views import login_required_custom
from apps.accounts.models import User
from apps.category_skills.models import SkillsCategory
from django.contrib import messages

def BlogView(request):
    blogs = Blog.objects.filter(is_published=True).select_related("author")

    custom_user = request.session.get("user_id")

    # Excludes the blogs from the current logged in users 
    if custom_user:
        blogs = blogs.exclude(author=custom_user)

    categories = SkillsCategory.objects.all().order_by("name")
    
    return render(request, "blog/blog.html", {"blogs": blogs , "categories":categories})

def BlogDetailView(request, pk):
    blog = get_object_or_404(Blog.objects.select_related("author").prefetch_related("sections"),pk=pk,is_published=True)
    sections = blog.sections.all().order_by("order")
    return render(request, "blog/blog-details.html", {"blog": blog, "sections": sections})

@login_required_custom
def BlogProfileView(request):

    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)

    user_blogs = Blog.objects.filter(author=user).order_by('-created_at')  # user's blogs
    
    context = {
        "custom_user": user,
        "user_blogs": user_blogs,
    }
    return render(request, "blog/blogs_profile.html", context)

@login_required_custom
def AddBlogView(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    categories = SkillsCategory.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        category_id = request.POST.get("category")
        intro = request.POST.get("intro")
        image = request.FILES.get("image")

        category = None
        if category_id:
            category = get_object_or_404(SkillsCategory, id=category_id)

        # Create Blog
        blog = Blog.objects.create(
            author=user,
            title=title,
            category=category,
            intro=intro,
            image=image,
        )

        # Create Blog Sections
        section_titles = request.POST.getlist("section_title[]")
        section_contents = request.POST.getlist("section_content[]")

        for idx, (sec_title, sec_content) in enumerate(zip(section_titles, section_contents)):
            if sec_title.strip() or sec_content.strip():
                BlogSection.objects.create(
                    blog=blog,
                    title=sec_title,
                    content=sec_content,
                    order=idx
                )

        messages.success(request, "Your blog has been published successfully!")
        return redirect("blog:blog-profile-view")

    context = {
        "custom_user": user,
        "categories": categories,
    }
    return render(request, "blog/add_blog.html", context)

@login_required_custom
def BlogEditView(request, pk):
    
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)

    blog = get_object_or_404(Blog, pk=pk, author=user)

    categories = SkillsCategory.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        category_id = request.POST.get("category")
        intro = request.POST.get("intro")
        image = request.FILES.get("image")

        # update blog fields
        blog.title = title
        blog.category_id = category_id
        blog.intro = intro
        if image:
            blog.image = image
        blog.save()

        # clear existing sections
        blog.sections.all().delete()

        # add new sections
        section_titles = request.POST.getlist("section_title[]")
        section_contents = request.POST.getlist("section_content[]")
        for order, (stitle, scontent) in enumerate(zip(section_titles, section_contents)):
            if stitle.strip() or scontent.strip():
                BlogSection.objects.create(
                    blog=blog,
                    title=stitle,
                    content=scontent,
                    order=order
                )

        messages.success(request, "Blog updated successfully ✅")
        return redirect("blog:blog-profile-view")

    context = {
        "blog": blog,
        "categories": categories,
        "sections": blog.sections.all().order_by("order"),
    }
    return render(request, "blog/edit_blog.html", context)