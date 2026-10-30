from rest_framework import serializers

from accounts.serializers import UserPublicSerializer
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