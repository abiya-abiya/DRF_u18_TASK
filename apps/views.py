from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.reverse import reverse

from apps.models import Project, ProjectMember
from apps.serializers import ProjectSerializer
from task.models import Task
from task_manager.permissions import IsProjectAdmin, IsProjectOwner


# Create your views here.
# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         user = self.request.user
#         return Project.objects.filter(
#             Q(owner=user) | Q(members=user)
#
#         ).distinct()
#
#     def perform_create(self, serializer):
#         project = serializer.save(owner=self.request.user)
#         ProjectMember.objects.create(
#             project = project,
#             user = self.request.user,
#             role=ProjectMember.Role.ADMIN
#         )


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
# yo'q → 405
    filterset_fields = ['visibility']
    search_fields = ['name']
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Project.objects.none()
        return (
            Project.objects.
            visible_to(self.request.user)
            .select_related('owner')
)# R: kim nimani ko'radi
    def perform_create(self, serializer):
        with transaction.atomic():
        # hammasi yoki hech narsa
            project = serializer.save(owner=self.request.user)
            ProjectMember.objects.create(
                project=project,
                user=self.request.user,
                role=ProjectMember.Role.ADMIN,
            )
        # owner birinchi admin

    def test_delete_project_removes_tasks(self):
        self.login(self.owner)
        self.client.delete(reverse('project-detail', args=[self.private.pk]))
        self.assertFalse(Task.objects.filter(project_id=self.private.pk).exists())

    permission_by_action = {
        'partial_update': [IsAuthenticated, IsProjectAdmin],
        'destroy': [IsAuthenticated, IsProjectOwner],
        'add_member': [IsAuthenticated, IsProjectAdmin],
        'remove_member': [IsAuthenticated, IsProjectAdmin],
    }

    def get_permissions(self):
        classes = self.permission_by_action.get(self.action, [IsAuthenticated])
        return [permission() for permission in classes]










# class ProjectMemberViewSet(viewsets.ModelViewSet):
#     queryset = ProjectMember.objects.all()
#     serializer_class = ProjectMemberSerializer
#     permission_classes = [IsAuthenticated]
