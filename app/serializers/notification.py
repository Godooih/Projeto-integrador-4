from rest_framework import serializers
from ..models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification   #model de conversão
        fields = '__all__' #todos os campos
        many = True        #permite serialização de vários