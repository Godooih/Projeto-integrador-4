from rest_framework import serializers
from ..models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category   #model de conversão
        fields = '__all__' #todos os campos
        many = True        #permite serialização de vários