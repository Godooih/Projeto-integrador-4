from rest_framework import serializers
from ..models import Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    from .category import CategorySerializer
    from .environment import EnvironmentSerializer

    category_FK = CategorySerializer()
    environment_FK = EnvironmentSerializer()

    class Meta:
        model = Equipment   #model de conversão
        fields = '__all__' #todos os campos
        many = True        #permite serialização de vários