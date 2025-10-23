# Em seu arquivo de serializers/task.py

from rest_framework import serializers
from ..models import Task, TaskStatus, TaskStatusImage

# ... (Seus outros serializers CustomUserSerializer, etc., se estiverem no mesmo arquivo)

class TaskReadSerializer(serializers.ModelSerializer):
    from .custom_user import CustomUserSerializer

    # Mantemos os serializers para os dados dos usuários
    creator_FK = CustomUserSerializer()
    assignees_FK = CustomUserSerializer(many=True)

    # --- CAMPOS CUSTOMIZADOS PARA O FLUTTER ---
    # Estes campos não existem no model, nós os criamos aqui.
    equipment_name = serializers.SerializerMethodField()
    current_status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        # ATENÇÃO: Listamos os campos que o Flutter precisa.
        # Removemos 'equipments_FK' para não enviar dados desnecessários.
        fields = [
            'id', 
            'name', 
            'description', 
            'creation_date', 
            'urgency_level',
            'creator_FK',
            'assignees_FK',
            'equipment_name',  # Nosso novo campo
            'current_status',  # Nosso novo campo
        ]
        many = True

    def get_equipment_name(self, obj):
        """
        Esta função alimenta o campo 'equipment_name'.
        Ela pega o primeiro equipamento da lista da tarefa.
        """
        equipment = obj.equipments_FK.first()
        return equipment.name if equipment else 'N/A' # Retorna o nome ou 'N/A'

    def get_current_status(self, obj):
        """
        Esta função alimenta o campo 'current_status'.
        Ela busca o status mais recente associado à tarefa.
        """
        # Acessa os status relacionados através do 'related_name' do model
        latest_status = obj.TaskStatus_task_FK.order_by('-status_date').first()
        return latest_status.status if latest_status else 'OPEN' # Retorna o status ou 'OPEN' por padrão

# Seus outros serializers (TaskWriteSerializer, etc.) podem continuar como estão.
class TaskWriteSerializer(serializers.ModelSerializer):
    # Dizemos que o creator_FK não precisa ser enviado na requisição POST
    creator_FK = serializers.ReadOnlyField(source='creator_FK.name')

    class Meta:
        model = Task
        # Listamos todos os campos, exceto os que são automáticos (como creation_date)
        fields = [
            'id',
            'name',
            'description',
            'suggested_date',
            'urgency_level',
            'equipments_FK',
            'assignees_FK',
            'creator_FK', # Incluímos o campo de leitura aqui
        ]
        many = True

class TaskStatusSerializer(serializers.ModelSerializer):
    # ... (sem mudanças)
    class Meta:
        model = TaskStatus
        fields = '__all__'
        many = True

class TaskStatusImageSerializer(serializers.ModelSerializer):
    # ... (sem mudanças)
    class Meta:
        model = TaskStatusImage
        fields = '__all__'
        many = True