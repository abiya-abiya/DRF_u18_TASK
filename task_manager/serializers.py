from rest_framework import serializers

from accounts.serializers import UserPublicSerializer
from apps.models import ProjectMember
from task_manager.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(read_only=True)
    my_role = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'my_role',
                  'visibility', 'created_at']
        read_only_fields = ['id', 'created_at']

        def get_my_role(self, project):
            user = self.context['request'].user
            if project.owner == user.id:
                return 'owner'
            return getattr(project, 'membership_role', None)

class MemberSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    joined_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['role', 'user', 'joined_at']

class MemberCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    role