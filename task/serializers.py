from rest_framework import serializers

from accounts.serializers import UserPublicSerializer
from apps.models import ProjectMember
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserPublicSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'status', 'priority', 'created_by', 'assigned_to']
        read_only_fields = ['id', 'created_by']
    def validate(self, attrs):
        project = attrs.get('project') or getattr(self.instance, 'project', None) # PATCH dabody da yo'q
        assignee = attrs.get('assigned_to')
        if assignee and not ProjectMember.objects.filter(project=project,user=assignee).exists():
            raise serializers.ValidationError(
                {'assigned_to': "Bu foydalanuvchi loyiha a'zosi emas. Avval uni qo'shing."}
)
        return attrs