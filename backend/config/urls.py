from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/leads/", include("apps.leads.urls")),
    path("api/v1/projects/", include("apps.projects.urls")),
    path("api/v1/content/", include("apps.content.urls")),
    path("api/v1/tools/", include("apps.tools.urls")),
]
