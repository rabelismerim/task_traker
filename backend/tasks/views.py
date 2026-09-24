from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas as tarefas do usuário autenticado
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Atribui automaticamente o usuário logado ao campo owner ao salvar
        serializer.save(owner=self.request.user)