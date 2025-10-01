from rest_framework import serializers
from ..models import CustomUser
from rest_framework.relations import SlugRelatedField

class CustomUserSerializer(serializers.ModelSerializer):
    groups = SlugRelatedField(
        many = True,
        read_only = True,
        slug_field = 'name',
    )

    class Meta:
        model = CustomUser   #model de conversão
        fields = ('id','email','name','photo','groups',) #todos os campos
        many = True        #permite serialização de vários