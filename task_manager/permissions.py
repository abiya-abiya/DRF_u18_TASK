from rest_framework.permissions import BasePermission

from apps.models import ProjectMember


def get_member_role(project, user):
    if project.owner_id == user.id:
        return 'owner'
    return (
        ProjectMember.objects
        .filter(project=project, user=user)
        .values_list('role', flat=True)
        .first()
    )

class IsProjectAdmin(BasePermission):
    massage = 'Faqat loyiha admini yoki egasi'

    def has_object_permission(self, request, view, project):
        return get_member_role(project, request.user) in ('owner', 'admin')

class IsProjectOwner(BasePermission):
    massage = 'Faqat loyiha egasi'

    def has_object_permission(self, request, view, project):
        return project.owner_id == request.user.id