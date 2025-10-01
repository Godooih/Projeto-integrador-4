from rest_framework.viewsets import ModelViewSet
from ..models import CustomUser
from ..serializers import CustomUserSerializer

class CustomUserView(ModelViewSet):
    queryset = CustomUser.objects.all() #qual a tabela e a query
    serializer_class = CustomUserSerializer #qual o serializer