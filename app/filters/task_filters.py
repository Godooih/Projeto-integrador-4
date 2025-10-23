import django_filters
from ..models import Task

class TaskFilters(django_filters.FilterSet):
    urgency_level = django_filters.CharFilter(field_name='urgency_level',lookup_expr='iexact')
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description',lookup_expr='iexact')
    creation_date = django_filters.DateFromToRangeFilter(lookup_expr='iexact')

    class Meta:
        model = Task
        fields = ['name','description','creation_date','urgency_level']