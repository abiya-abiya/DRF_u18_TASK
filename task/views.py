from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from task.models import Task
from task.serializers import TaskSerializer


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['project', 'status', 'priority', 'assigned_to']

    search_field = ['title', 'description']

    ordering_fields = ['created_at', 'due_date']

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(owner=user) | Q(member=user)

        ).distinct()


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)