# app/views.py (VERSÃO CORRIGIDA)

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response

# --- 1. IMPORTS DOS MODELS ---
from .models import (
    Category, 
    CustomUser, 
    Environment, 
    Equipment, 
    Notification, 
    TaskStatus, 
    TaskStatusImage, 
    Task
)

# --- 2. IMPORTS CORRETOS DOS SERIALIZERS ---
# (Importando TODAS as classes que vamos usar)
from .serializers import (
    CategorySerializer, 
    CustomUserSerializer, 
    EnvironmentSerializer, 
    EquipmentReadSerializer, 
    EquipmentWriteSerializer,      # <-- Faltava este
    EquipmentSearchSerializer,     # <-- Faltava este
    NotificationSerializer, 
    TaskStatusSerializer, 
    TaskStatusImageSerializer, 
    TaskReadSerializer,
    TaskWriteSerializer,           # <-- Faltava este
    ReadWriteSerializer            # <-- Faltava este (o mais importante)
)

# --- 3. IMPORTS DOS UTILS (se você os tiver) ---
try:
    from .utils import isAdmin
    from .filters import TaskFilters
except ImportError:
    # Se os arquivos não existirem, crie funções placeholder
    # para o servidor não quebrar.
    def isAdmin(user_id):
        return False # Mude para True se quiser testar como admin
    
    # Crie um TaskFilters básico se ele não existir
    from django_filters import rest_framework as filters
    class TaskFilters(filters.FilterSet):
        class Meta:
            model = Task
            fields = ['urgency_level', 'assignees_FK']


# --- 4. SUAS VIEWS (CORRIGIDAS) ---

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomUserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class EnvironmentView(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer

# --- CORRIGIDO: EquipmentView ---
# Precisa herdar de ReadWriteSerializer
class EquipmentView(ReadWriteSerializer, viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    
    # Define os serializers de leitura e escrita
    read_serializer_class = EquipmentReadSerializer
    write_serializer_class = EquipmentWriteSerializer
    
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code']

    # Opcional: usa o serializer leve para a lista
    def get_serializer_class(self):
        if self.action == 'list':
            return EquipmentSearchSerializer
        return super().get_serializer_class() 

class NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class TaskStatusView(viewsets.ModelViewSet):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_FK']

    def perform_create(self, serializer):
        # Grava automaticamente o usuário logado como autor da mudança
        serializer.save(user_FK=self.request.user)

class TaskStatusImageView(viewsets.ModelViewSet):
    queryset = TaskStatusImage.objects.all()
    serializer_class = TaskStatusImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_FK']

# --- CORRIGIDO: TaskView ---
# Precisa herdar de ReadWriteSerializer para que o write_serializer_class funcione!
class TaskView(ReadWriteSerializer, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    
    # Define os serializers de leitura e escrita
    read_serializer_class = TaskReadSerializer
    write_serializer_class = TaskWriteSerializer # <-- Agora esta linha vai funcionar!
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TaskFilters
    ordering_fields = '__all__'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if isAdmin(user.id): 
                return Task.objects.all().order_by('-creation_date')
            return Task.objects.filter(creator_FK=user).order_by('-creation_date')
        return Task.objects.none()
        pass
    
    def perform_create(self, serializer):
        # Esta função só é chamada se o TaskWriteSerializer for válido.
        task = serializer.save(creator_FK=self.request.user)
        TaskStatus.objects.create(
            task_FK=task, 
            user_FK=self.request.user,
            comment="Chamado criado com sucesso."
        )
        pass

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve o método DELETE para adicionar regras de negócio.
        """
        task = self.get_object()
        user = self.request.user

        # REGRA 1: Somente o criador do chamado pode excluí-lo.
        if task.creator_FK != user:
            return Response(
                {"detail": "Você não tem permissão para excluir este chamado."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # REGRA 2: Verifica o status atual do chamado.
        # (Buscamos o status mais recente)
        latest_status_obj = task.TaskStatus_task_FK.order_by('-status_date').first()
        current_status = latest_status_obj.status if latest_status_obj else 'OPEN' # Default 'OPEN'

        # Defina os status que BLOQUEIAM a exclusão
        # (Use os nomes exatos que você salva no banco, ex: 'IN_PROGRESS', 'DONE')
        NON_DELETABLE_STATUSES = ['IN_PROGRESS', 'EM ANDAMENTO', 'DONE', 'CONCLUÍDO']

        if current_status.upper() in NON_DELETABLE_STATUSES:
            return Response(
                {"detail": "Não é possível excluir um chamado que já está em andamento ou foi concluído."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Se passou nas regras, exclui o chamado.
        return super().destroy(request, *args, **kwargs)