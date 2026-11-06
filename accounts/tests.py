from django.test import TestCase
from django.db import IntegrityError, transaction

from accounts.models import CustomUser
from apps.models import Project, ProjectMember
from task.models import Task

from rest_framework.test import APITestCase
from django.test import TestCase
import shutil, tempfile
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image

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

MEDIA_TMP = tempfile.mkdtemp()
def png_bytes():
    buffer = BytesIO()
    Image.new('RGB', (1, 1), 'red').save(buffer, 'PNG')
    return buffer.getvalue()


@override_settings(MEDIA_ROOT=MEDIA_TMP)
class AvatarUploadTests(APITestCase):
    def test_register_with_avatar_stores_file_under_avatars(self):
        avatar = SimpleUploadedFile('me.png', png_bytes(), content_type='image/png')
        response = self.client.post(
        '/api/v1/auth/register/',
        {'username': 'ali', 'email': 'ali@example.com', 'password': 'Str0ng-pass-2026',
        'avatar': avatar},
        format='multipart',
        )
        self.assertEqual(response.status_code, 201, response.data)
        user = CustomUser.objects.get(username='ali')
        self.assertTrue(user.avatar.name.startswith('avatars/'))
