from django.db import transaction

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.serializers import ProjectSerializer

from apps.models import Project, ProjectMember

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
            .visible_to(self.request.user)
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

    @action(detail=True, methods=['delete'],
            url_path=r'members/(?P<user_id>\d+)', url_name='member-detail')
    def remove_member(self, request, pk=None, user_id=None):
        project = self.get_object()  # IsProjectAdmin

        membership = get_object_or_404(ProjectMember, project=project, user_id=user_id)
        if membership.user_id == project.owner_id:
            raise ValidationError({'detail': 'Cannot modify project owner'})
        if membership.user_id == request.user.id:
            raise ValidationError({'detail': 'Use leave to exit the project'})
        with transaction.atomic():
            project.tasks.filter(assigned_to_id=user_id).update(assigned_to=None)
            membership.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])  # projects/{pk}/leave/
    def leave(self, request, pk=None):
        project = self.get_object()  # faqat IsAuthenticated

        if project.owner_id == request.user.id:
            raise ValidationError({'detail': 'Owner cannot leave the project'})
        membership = get_object_or_404(ProjectMember, project=project, user=request.user)
        with transaction.atomic():
            project.tasks.filter(assigned_to=request.user).update(assigned_to=None)
            membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)