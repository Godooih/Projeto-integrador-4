from rest_framework.viewsets import ModelViewSet
from ..models import Task, TaskStatus, TaskStatusImage
from ..serializers import TaskSerializer, TaskStatusSerializer, TaskStatusImageSerializer

class TaskView(ModelViewSet):
    queryset = Task.objects.all() #qual a tabela e a query
    serializer_class = TaskSerializer #qual o serializer

class TaskStatusView(ModelViewSet):
    queryset = TaskStatus.objects.all() #qual a tabela e a query
    serializer_class = TaskStatusSerializer #qual o serializer

class TaskStatusImageView(ModelViewSet):
    queryset = TaskStatusImage.objects.all() #qual a tabela e a query
    serializer_class = TaskStatusImageSerializer #qual o serializer