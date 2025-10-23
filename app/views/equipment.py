# Em views/equipment.py

from rest_framework import viewsets
from rest_framework.filters import SearchFilter # <-- 1. Importe o SearchFilter
from django_filters.rest_framework import DjangoFilterBackend # Se quiser filtros mais avançados no futuro
from ..models import Equipment
# 👇 2. Importe o novo serializer que criamos
from ..serializers import EquipmentReadSerializer, EquipmentWriteSerializer, EquipmentSearchSerializer, ReadWriteSerializer

class EquipmentView(ReadWriteSerializer, viewsets.ModelViewSet):
    # ... seu código existente ...
    queryset = Equipment.objects.all()
    read_serializer_class = EquipmentReadSerializer
    write_serializer_class = EquipmentWriteSerializer

    # ✅ --- NOSSA NOVA LÓGICA DE BUSCA ---
    # 3. Adicione estas linhas para habilitar a busca
    filter_backends = [SearchFilter]
    # 4. Diga ao Django em quais campos ele deve procurar
    search_fields = ['name', 'code']

    # 5. Opcional, mas recomendado: use o serializer leve para a listagem
    def get_serializer_class(self):
        if self.action == 'list':
            return EquipmentSearchSerializer
        return super().get_serializer_class()