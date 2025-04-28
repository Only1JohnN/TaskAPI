import django_filters
from .models import TaskModel

class TaskFilter(django_filters.FilterSet):
    start_date = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='lte')
    # status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = TaskModel
        fields = ['start_date', 'end_date', 'completed', 'priority', 'tags']
