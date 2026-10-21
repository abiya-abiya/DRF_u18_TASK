from rest_framework import serializers

from apps.models import Project, ProjectMember


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'owner',
            'visibility',
            'members',
        ]
        read_only_fields = ['owner']

class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = [
            'id',
            'project',
            'user',
            'role',
            'join_date',
            'left_date',

        ]