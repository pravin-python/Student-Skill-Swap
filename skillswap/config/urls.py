from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',include('apps.core.urls')),
    path('',include('apps.category_skills.urls')),
    path('',include('apps.accounts.urls')),
    path('notifications/',include('apps.notifications.urls')),
    path('universities/',include('apps.university.urls')),
    path('',include('apps.api.urls')),
    path('',include('apps.blog.urls')),
]+static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)