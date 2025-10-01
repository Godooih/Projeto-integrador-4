from rest_framework.viewsets import ModelViewSet
from ..models import Environment
from ..serializers import EnvironmentSerializer

class EnvironmentView(ModelViewSet):
    queryset = Environment.objects.all() #qual a tabela e a query
    serializer_class = EnvironmentSerializer #qual o serializer