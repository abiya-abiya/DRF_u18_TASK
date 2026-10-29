from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from apps.models import Project, ProjectMember
from apps.serializers import ProjectSerializer


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


    def get_permissions(self):
        ...










# class ProjectMemberViewSet(viewsets.ModelViewSet):
#     queryset = ProjectMember.objects.all()
#     serializer_class = ProjectMemberSerializer
#     permission_classes = [IsAuthenticated]
