from rest_framework import serializers

from apps.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'owner',
            'visibility',
            'members',
        ]
        read_only_fields = ['owner']