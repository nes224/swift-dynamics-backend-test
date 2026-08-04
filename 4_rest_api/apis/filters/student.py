import django_filters
from apis.models import Student


class StudentFilter(django_filters.FilterSet):
    school = django_filters.NumberFilter(field_name='classroom__school_id')
    school_id = django_filters.NumberFilter(field_name='classroom__school_id')
    classroom = django_filters.NumberFilter(field_name='classroom_id')
    classroom_id = django_filters.NumberFilter(field_name='classroom_id')
    gender = django_filters.CharFilter(field_name='gender')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['school', 'school_id', 'classroom', 'classroom_id', 'gender', 'first_name', 'last_name']