from django.test import TestCase
from django.db import IntegrityError, transaction

from accounts.models import CustomUser
from apps.models import Project, ProjectMember
from task.models import Task


class TaskAssigneeTests(TestCase):
    def test_task_survives_assignee_deletion(self):
        owner = CustomUser.objects.create_user(username='owner',
    email='o@example.com')
        worker = CustomUser.objects.create_user(username='worker',
    email='w@example.com')
        project = Project.objects.create(name='P', owner=owner)
        task = Task.objects.create(project=project, title='T', created_by=owner,
    assigned_to=worker)
        worker.delete()
        task.refresh_from_db()
        self.assertIsNone(task.assigned_to)
class ProjectMemberConstraintTests(TestCase):
    def test_user_cannot_join_same_project_twice(self):
        owner = CustomUser.objects.create_user(username='owner',
        email='o@example.com')
        user = CustomUser.objects.create_user(username='vali', email='v@example.com')
        project = Project.objects.create(name='P', owner=owner)
        ProjectMember.objects.create(project=project, user=user)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ProjectMember.objects.create(project=project, user=user)
        self.assertEqual(ProjectMember.objects.filter(project=project,
        user=user).count(), 1)
