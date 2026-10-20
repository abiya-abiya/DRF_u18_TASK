from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.views import ProjectViewSet, ProjectMemberViewSet

router = DefaultRouter()

router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-members', ProjectMemberViewSet, basename='project_member')

urlpatterns = [
    path('', include(router.urls)),
]


