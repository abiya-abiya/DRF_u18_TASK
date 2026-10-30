from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets

from apps.models import ProjectMember
from apps.serializers import ProjectSerializer
from task_manager.models import Project


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filterset_fields = ['visibility']
    search_fields = ['name']

    def get_queryset(self):
        return (
            Project.objects
            .visibile_to(self.request.user)
            .select_related('owner')
        )

    def perform_create(self, serializer):
        with transaction.atomic():
            project = serializer.save(owner=self.request.user)
            ProjectMember.objects.create(
                project=project,
                user=self.request.user,
                role = ProjectMember.Role.ADMIN,
            )

    def perform_update(self, serializer):
        ...