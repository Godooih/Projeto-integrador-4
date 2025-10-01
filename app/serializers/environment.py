from rest_framework import serializers
from ..models import Environment

class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment   #model de conversão
        fields = '__all__' #todos os campos
        many = True        #permite serialização de vários