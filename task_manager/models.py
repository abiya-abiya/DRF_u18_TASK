from apps.models import ProjectQuerySet
from common.models import TimeStampedModel



class Project(TimeStampedModel):
    ...
    objects = ProjectQuerySet.as_manager()