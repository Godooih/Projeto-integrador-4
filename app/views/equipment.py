from rest_framework.viewsets import ModelViewSet
from ..models import Equipment
from ..serializers import EquipmentSerializer

class EquipmentView(ModelViewSet):
    queryset = Equipment.objects.all() #qual a tabela e a query
    serializer_class = EquipmentSerializer #qual o serializer