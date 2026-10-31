from django.db import models
from django.db.models import Q

from accounts.models import CustomUser
from common.models import TimeStampedModel


class ProjectQuerySet(models.QuerySet):
    def visible_to(self, user):
        if user.is_anonymous:
            return self.none()

        return self.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()


class Project(TimeStampedModel):
    class Visibility(models.TextChoices):
        PRIVATE = 'private', 'Private'
        PUBLIC = 'public', 'Public'

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='owned_projects',
    )
    visibility = models.CharField(
        max_length=7,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
    )
    members = models.ManyToManyField(
        CustomUser,
        through='ProjectMember',
        related_name='projects',
        blank=True,
    )

    # Manager'ni ulash
    objects = ProjectQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProjectMember(TimeStampedModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MEMBER = 'member', 'Member'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_members',
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='project_memberships',
    )
    role = models.CharField(
        max_length=6,
        choices=Role.choices,
        default=Role.MEMBER,
    )
    join_date = models.DateField(blank=True, null=True)
    left_date = models.DateField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                name='unique_project_member',
            ),
        ]

    def __str__(self):
        return f'{self.user} - {self.project}'