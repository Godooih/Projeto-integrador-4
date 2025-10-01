from rest_framework.viewsets import ModelViewSet
from ..models import Notification
from ..serializers import NotificationSerializer

class NotificationView(ModelViewSet):
    queryset = Notification.objects.all() #qual a tabela e a query
    serializer_class = NotificationSerializer #qual o serializer