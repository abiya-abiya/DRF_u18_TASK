from unittest import TestCase

from accounts.models import CustomUser
from apps.models import ProjectMember
from task_manager.models import Project
from task_manager.permissions import get_member_role


class MemberRoleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = CustomUser.objects.create_user(username='owner', email='owner@example.com')
        cls.admin = CustomUser.objects.create_user(username='admin', email='admin@example.com')
        cls.stranger = CustomUser.objects.create_user(username='stranger', email='stranger@example.com')
        cls.project = Project.objects.create(name='P', owner=cls.owner)
        ProjectMember.objects.create(project=cls.project, user=cls.admin, role=ProjectMember.Role.ADMIN)

    def test_owner_role_comes_from_owner_field(self):
        self.assertEqual(get_member_role(self.project, self.owner), 'owner')

    def test_admin_role_comes_from_membership(self):
        self.assertEqual(get_member_role(self.project, self.admin), 'admin')

    def test_stranger_has_no_role(self):
        self.assertIsNone(get_member_role(self.project, self.stranger))

    def test_owner_lookup_makes_no_query(self):
        with self.assertNumQueries(0):
            get_member_role(self.project, self.owner)
