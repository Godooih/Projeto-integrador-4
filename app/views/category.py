from rest_framework.viewsets import ModelViewSet
from ..models import Category
from ..serializers import CategorySerializer

class CategoryView(ModelViewSet):
    queryset = Category.objects.all() #qual a tabela e a query
    serializer_class = CategorySerializer #qual o serializer