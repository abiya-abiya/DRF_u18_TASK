from django.db import models
from accounts.models import  CustomUser
from apps.models import Project
from common.models import TimeStampedModel
from config import settings


# Create your models here.
class Task(TimeStampedModel):
    class Status(models.TextChoices):
        TODO = 'todo', 'ToDo'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=11,
        choices=Status.choices,
        default=Status.TODO
    )
    priority = models.CharField(
        max_length=6,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # yoki CustomUser
        on_delete=models.SET_NULL,  # <--- CASCADE o'rniga SET_NULL bo'lishi kerak
        null=True,  # <--- SET_NULL ishlashi uchun null=True majburiy
        blank=True,
        related_name='tasks_assigned'
    )
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['status', '-created_at']

    def __str__(self):
        return self.title
