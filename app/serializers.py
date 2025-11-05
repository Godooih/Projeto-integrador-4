# app/serializers.py (VERSÃO CORRIGIDA E REORDENADA)

from rest_framework import serializers
from .models import (
    Task, 
    TaskStatus, 
    TaskStatusImage,
    Category,
    CustomUser,
    Environment,
    Equipment,
    Notification
)
from rest_framework.relations import SlugRelatedField

# --- 1. CLASSES UTILITÁRIAS E "BASE" ---
# (Classes que não dependem de outros serializers)

class ReadWriteSerializer(object):
    """
    Mixin para permitir serializers de leitura (Read) e escrita (Write)
    diferentes na mesma ViewSet.
    """
    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        if self.action in ['create','update', 'partial_update','destroy']:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()
    
    def get_read_serializer_class(self):
        return self.read_serializer_class
    
    def get_write_serializer_class(self):
        return self.write_serializer_class

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    groups = SlugRelatedField(
        many = True,
        read_only = True,
        slug_field = 'name',
    )

    class Meta:
        model = CustomUser
        fields = ('id','email','name','photo','groups',)

class EquipmentSearchSerializer(serializers.ModelSerializer):
    """
    Serializer leve para a busca de equipamentos (usado no Flutter).
    """
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'code']

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'

class TaskStatusImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusImage
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


# --- 2. SERIALIZERS DE "LEITURA" (READ) ---
# (Dependem das classes "base" acima)

class EquipmentReadSerializer(serializers.ModelSerializer):
    category_FK = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    environment_FK = EnvironmentSerializer()

    class Meta:
        model = Equipment
        fields = '__all__'


class TaskReadSerializer(serializers.ModelSerializer):
    creator_FK = CustomUserSerializer()
    assignees_FK = CustomUserSerializer(many=True)
    equipment_name = serializers.SerializerMethodField()
    current_status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 
            'name', 
            'description', 
            'creation_date', 
            'urgency_level',
            'creator_FK',
            'assignees_FK',
            'equipment_name',
            'current_status',
        ]

    def get_equipment_name(self, obj):
        equipment = obj.equipments_FK.first()
        return equipment.name if equipment else 'N/A'

    def get_current_status(self, obj):
        try:
            latest_status = obj.TaskStatus_task_FK.order_by('-status_date').first()
            return latest_status.status if latest_status else 'OPEN'
        except AttributeError:
            return 'OPEN' 

# --- 3. SERIALIZERS DE "ESCRITA" (WRITE) ---

class EquipmentWriteSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Equipment
        fields = '__all__'


# 🚨 ESTA É A CLASSE QUE CORRIGE O SEU ERRO 🚨
class TaskWriteSerializer(serializers.ModelSerializer):
    """
    Serializer de ESCRITA: Usado para criar e atualizar chamados.
    Resolve o erro de validação do Flutter.
    """
    
    # --- CORREÇÃO 1: "assignees_FK" ---
    # Aceita uma lista de IDs (chaves primárias)
    assignees_FK = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.all(),
        required=False # Torna opcional
    )

    # --- CORREÇÃO 2: "equipments_FK" ---
    # Aceita uma lista de IDs (chaves primárias)
    equipments_FK = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Equipment.objects.all()
    )
    
    # --- CORREÇÃO 3: "creator_FK" ---
    # Torna o campo 'read_only' (somente leitura).
    # A view (perform_create) vai preenchê-lo.
    creator_FK = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Task
        fields = [
            'name', 
            'description', 
            'suggested_date', 
            'urgency_level', 
            'equipments_FK', 
            'assignees_FK',
            'creator_FK', # <-- Importante manter na lista
        ]