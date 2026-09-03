from django.db import transaction
from django.utils.text import slugify

from .models import AuditLog, Workspace, WorkspaceMembership


def unique_workspace_slug(name):
    base = slugify(name) or "workspace"
    slug = base
    suffix = 2
    while Workspace.objects.filter(slug=slug).exists():
        slug = f"{base}-{suffix}"
        suffix += 1
    return slug


@transaction.atomic
def create_workspace(*, owner, name):
    workspace = Workspace.objects.create(
        name=name.strip(),
        slug=unique_workspace_slug(name),
        owner=owner,
    )
    WorkspaceMembership.objects.create(
        workspace=workspace,
        user=owner,
        role=WorkspaceMembership.ROLE_OWNER,
    )
    return workspace


def user_workspaces(user):
    return Workspace.objects.filter(
        memberships__user=user,
        memberships__is_active=True,
        is_active=True,
    ).distinct()


def write_audit_log(*, action, actor=None, workspace=None, resource_type="", resource_id="", metadata=None, request=None):
    ip_address = None
    user_agent = ""
    if request is not None:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        ip_address = forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:2000]

    return AuditLog.objects.create(
        action=action,
        actor=actor,
        workspace=workspace,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id else "",
        metadata=metadata or {},
        ip_address=ip_address,
        user_agent=user_agent,
    )
