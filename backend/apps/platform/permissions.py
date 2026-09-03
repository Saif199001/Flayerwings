from rest_framework.permissions import BasePermission

from .models import WorkspaceMembership


class IsWorkspaceMember(BasePermission):
    message = "You are not a member of this workspace."

    def has_permission(self, request, view):
        workspace = getattr(view, "workspace", None)
        if workspace is None:
            workspace_id = request.data.get("workspace") or request.query_params.get("workspace")
            if not workspace_id:
                return False
            try:
                from .models import Workspace
                workspace = Workspace.objects.get(id=workspace_id, is_active=True)
            except (Workspace.DoesNotExist, ValueError):
                return False
        return WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=request.user,
            is_active=True,
        ).exists()


def has_workspace_role(user, workspace, roles):
    return WorkspaceMembership.objects.filter(
        workspace=workspace,
        user=user,
        is_active=True,
        role__in=roles,
    ).exists()
