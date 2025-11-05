# app/views.py
from rest_framework import viewsets
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
from .serializers import (
    CategorySerializer, 
    CustomUserSerializer, 
    EnvironmentSerializer, 
    EquipmentReadSerializer, 
    NotificationSerializer, 
    TaskStatusSerializer, 
    TaskStatusImageSerializer, 
    TaskReadSerializer
)

# --- Suas Views ---

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomUserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class EnvironmentView(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer

class EquipmentView(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentReadSerializer

class NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# --- A VIEW QUE ESTAVA FALTANDO ---
# O erro "AttributeError: ... has no attribute 'TaskStatusView'"
# aconteceu porque esta classe não existia no seu arquivo.
class TaskStatusView(viewsets.ModelViewSet):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer

# --- As outras views ---
class TaskStatusImageView(viewsets.ModelViewSet):
    queryset = TaskStatusImage.objects.all()
    serializer_class = TaskStatusImageSerializer

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskReadSerializer