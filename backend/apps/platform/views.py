from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Workspace, WorkspaceMembership
from .serializers import WorkspaceMembershipSerializer, WorkspaceSerializer
from .services import create_workspace, user_workspaces, write_audit_log


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def workspace_list_create(request):
    if request.method == "GET":
        serializer = WorkspaceSerializer(
            user_workspaces(request.user),
            many=True,
            context={"request": request},
        )
        return Response({"data": serializer.data})

    name = str(request.data.get("name", "")).strip()
    if not name:
        return Response({"name": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    workspace = create_workspace(owner=request.user, name=name)
    write_audit_log(
        action="workspace.created",
        actor=request.user,
        workspace=workspace,
        resource_type="workspace",
        resource_id=workspace.id,
        request=request,
    )
    return Response(
        WorkspaceSerializer(workspace, context={"request": request}).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workspace_detail(request, workspace_id):
    try:
        workspace = user_workspaces(request.user).get(id=workspace_id)
    except (Workspace.DoesNotExist, ValueError):
        return Response({"detail": "Workspace not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response({
        "workspace": WorkspaceSerializer(workspace, context={"request": request}).data,
        "members": WorkspaceMembershipSerializer(
            workspace.memberships.filter(is_active=True).select_related("user"),
            many=True,
        ).data,
    })
