from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Retorna apenas as tarefas do utilizador autenticado
        return Task.objects.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        # Associa automaticamente o utilizador logado à tarefa
        serializer.save(user=self.request.user)