# Em seu arquivo de views/task.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task, TaskStatus  # <-- Importe o TaskStatus
from .serializers import TaskReadSerializer, TaskWriteSerializer, ReadWriteSerializer

class TaskViewSet(ReadWriteSerializer, viewsets.ModelViewSet):
    """
    ViewSet para visualizar e editar Tarefas (Chamados).
    """
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all().order_by('-creation_date')
    read_serializer_class = TaskReadSerializer
    write_serializer_class = TaskWriteSerializer

    # ✅ --- NOSSA NOVA LÓGICA VAI AQUI ---
    def perform_create(self, serializer):
        """
        Salva um novo chamado e cria seu status inicial.
        """
        # 1. Salva o chamado, injetando o usuário logado como o criador.
        #    O `self.request.user` pega o usuário que fez a requisição.
        task = serializer.save(creator_FK=self.request.user)

        # 2. Cria o primeiro status para este chamado.
        #    Por padrão, será 'OPEN'.
        TaskStatus.objects.create(
            task_FK=task, 
            user_FK=self.request.user,
            comment="Chamado criado com sucesso." # Um comentário opcional
        )