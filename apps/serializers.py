from rest_framework import serializers

from accounts.serializers import UserPublicSerializer
from apps.models import Project, ProjectMember


# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = [
#             'id',
#             'name',
#             'description',
#             'owner',
#             'visibility',
#             'members',
#         ]
#         read_only_fields = ['owner']
#
# class ProjectMemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectMember
#         fields = [
#             'id',
#             'project',
#             'user',
#             'role',
#             'join_date',
#             'left_date',
#
#         ]


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(read_only=True)
    my_role = serializers.SerializerMethodField()
# ichma-ich, faqat o'qish
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'visibility', 'owner', 'my_role', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_my_role(self, project):
        user = self.context['request'].user
        if project.owner_id == user.id:
            return 'owner'
        return getattr(project, 'membership_role', None)

