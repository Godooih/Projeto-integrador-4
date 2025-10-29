# Em seu arquivo de views.py

from rest_framework.viewsets import ModelViewSet
from ..models import Task, TaskStatus, CustomUser
from ..serializers import ReadWriteSerializer, TaskReadSerializer, TaskWriteSerializer
from rest_framework.permissions import IsAuthenticated
from ..utils import isAdmin
from ..filters import TaskFilters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

# (Suas outras views como TaskStatusView, etc. podem continuar como estão)

class TaskView(ReadWriteSerializer, ModelViewSet):
    """
    ViewSet unificada para visualizar e editar Tarefas (Chamados).
    """
    queryset = Task.objects.all()
    read_serializer_class = TaskReadSerializer
    write_serializer_class = TaskWriteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TaskFilters
    ordering_fields = '__all__'

    def get_queryset(self):
        """
        Filtra os chamados:
        - Admin vê tudo.
        - Usuário normal vê apenas os que ele criou.
        """
        user = self.request.user
        if user.is_authenticated:
            if isAdmin(user.id):
                return Task.objects.all().order_by('-creation_date')
            return Task.objects.filter(creator_FK=user).order_by('-creation_date')
        return Task.objects.none()
    
    def perform_create(self, serializer):
        """
        Salva um novo chamado e cria seu status inicial.
        """
        # 1. Salva o chamado, injetando o usuário logado como o criador.
        #    O self.request.user JÁ É o objeto CustomUser, não precisa de outra consulta.
        task = serializer.save(creator_FK=self.request.user)

        # 2. Cria o primeiro status para este chamado (Status: OPEN).
        TaskStatus.objects.create(
            task_FK=task, 
            user_FK=self.request.user,
            comment="Chamado criado com sucesso."
            # O status padrão 'OPEN' será pego do seu model.
        )