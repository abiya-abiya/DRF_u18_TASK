from rest_framework import serializers

from accounts.models import CustomUser
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
    role = serializers.CharField(choices=ProjectMember.Role.choices, default='member')

    def validate_username(self, value):
        user = CustomUser.objects.get(username=value, is_active=True).first()
        if user is None:
            raise serializers.ValidationError('User not found')
        if ProjectMember.objects.filter(user=user, role=self.context['request'].role).exists():
            raise serializers.ValidationError('Username already exists')
        self.member_user = user
        return value

    def create(self, validated_data):
        return ProjectMember.objects.create(
            project=self.context['request'],
            user = self.member_user,
            role=validated_data['role'],
        )