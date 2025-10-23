from rest_framework.viewsets import ModelViewSet
from ..models import Task, TaskStatus, TaskStatusImage, CustomUser
from ..serializers import ReadWriteSerializer, TaskReadSerializer, TaskWriteSerializer, TaskStatusSerializer, TaskStatusImageSerializer
from rest_framework.permissions import IsAuthenticated
from ..utils import isAdmin
from ..filters import TaskFilters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class TaskView(ReadWriteSerializer, ModelViewSet):
    #select * from Task;
    queryset = Task.objects.all() #qual a tabela e a query
    read_serializer_class = TaskReadSerializer #qual o serializer
    write_serializer_class = TaskWriteSerializer #qual o serializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]    
    filterset_class = TaskFilters
    ordering_fields = '__all__'

    def get_queryset(self):
        items = self.request.GET.items()
        for item in items:
            print(f'parameters: {item}')
        user = self.request.user
        #select * from Task WHERE creator_FK = user.id
        if user.is_authenticated:
            return Task.objects.all() if isAdmin(user.id) \
                else Task.objects.filter(creator_FK=user.id)
        return Task.objects.none()
    

    def perform_create(self, serializer):
        user = self.request.user
        custom_user = CustomUser.objects.get(id=user.id)
        serializer.save(creator_FK=custom_user)

    

class TaskStatusView(ModelViewSet):
    queryset = TaskStatus.objects.all() #qual a tabela e a query
    serializer_class = TaskStatusSerializer #qual o serializer

class TaskStatusImageView(ModelViewSet):
    queryset = TaskStatusImage.objects.all() #qual a tabela e a query
    serializer_class = TaskStatusImageSerializer #qual o serializer