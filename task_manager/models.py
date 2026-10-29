from django.db import models
from django.db.models import Q

from apps.models import ProjectMember
from common.models import TimeStampedModel


# Create your models here.
class ProjectQuerySet(models.QuerySet):
    def visible_to(self, user):
        member_of = ProjectMember.objects.filter(user=user).values('project_id')
        return self.filter(
            Q(pk__in=member_of) | Q(visibility=Project.Visibility.PUBLIC) | Q(owner=user)
# yoki egasi men
)
class Project(TimeStampedModel):
    ...
    objects = ProjectQuerySet.as_manager()