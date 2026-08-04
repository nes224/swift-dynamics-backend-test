from apis.models import School
from django.db.models import Q

class SchoolService:
    @staticmethod
    def get_all_schools():
        return School.objects.all()

    @staticmethod
    def create_school(data: dict) -> School:
        if School.objects.filter(name=data.get('name')).exists():
            raise ValueError("School with this name already exists.")
        return School.objects.create(**data)

    @staticmethod
    def get_school_by_id(school_id: int):
        try:
            return School.objects.get(id=school_id)
        except School.DoesNotExist:
            return None

    @staticmethod
    def update_school(school: School, data: dict) -> School:
        for attr, value in data.items():
            setattr(school, attr, value)
        school.save()
        return school

    @staticmethod
    def delete_school_by_id(school_id: int):
        count, _ = School.objects.filter(id=school_id).delete()
        return count > 0

    @staticmethod
    def search_schools(
            keyword: str = None,
            filters: dict = None,
            ordering: str = None,
            limit: int = 10,
            offset: int = 0
        ):
        queryset = School.objects.all()
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(address__icontains=keyword)
            )

        if filters and isinstance(filters, dict):
            # กรองเฉพาะ key/value ที่ส่งมา
            clean_filters = {k: v for k, v in filters.items() if v is not None}
            queryset = queryset.filter(**clean_filters)

        if ordering:
            queryset = queryset.order_by(ordering)

        limit = limit if limit is not None else 10
        offset = offset if offset is not None else 0
        
        total_count = queryset.count()
        schools = queryset[offset:offset + limit]

        return schools, total_count