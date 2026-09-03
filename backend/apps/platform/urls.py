from django.urls import path

from .views import workspace_detail, workspace_list_create

urlpatterns = [
    path("workspaces/", workspace_list_create, name="workspace-list-create"),
    path("workspaces/<uuid:workspace_id>/", workspace_detail, name="workspace-detail"),
]
