from django.db import transaction
from django.shortcuts import render
from drf_yasg.openapi import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse

from apps.models import ProjectMember
from apps.serializers import ProjectSerializer
from task.models import Task
from task_manager.models import Project
from task_manager.permissions import IsProjectAdmin, IsProjectOwner
from task_manager.serializers import MemberSerializer, MemberCreateSerializer


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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def test_delete_project_removes_tasks(self):
        self.login(self.owner)
        self.client.delete(reverse('project-detail', args = [self.private.pk]))
        self.assertFalse(Task.objects.filter(project_id = self.private.pk).exists())

    permission_by_action = {
        'partial_update': [IsAuthenticated, IsProjectAdmin],
        'destroy': [IsAuthenticated, IsProjectOwner],
        'add_member': [IsAuthenticated, IsProjectAdmin],
        'remove_member': [IsAuthenticated, IsProjectAdmin],
    }
    def get_permissions(self):
        classes = self.permission_by_action.get(self.action, [IsAuthenticated])
        return [permission() for permission in classes]

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        project = self.get_object()
        qs = project.project_members.select_related('user').order_by('created_at')
        return Response(MemberSerializer(qs, many=True).data)

    @members.mapping.post
    def add_member(self, request, pk=None):
        project = self.get_object()
        serializer = MemberCreateSerializer(
            data=request.data,
            context={'request': request, 'project': project},
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)
