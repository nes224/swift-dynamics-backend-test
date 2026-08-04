from django.db.models import Q
from apis.models import Classroom

class ClassroomService:
    @staticmethod
    def get_classroom_by_id(classroom_id):
        try:
            return Classroom.objects.select_related('school').prefetch_related('teachers', 'students').get(id=classroom_id)
        except Classroom.DoesNotExist:
            return None

    @staticmethod
    def get_classroom_list(school_id=None, year=None, number=None):
        """สำหรับดึงรายการห้องเรียนทั้งหมด (เผื่อกรณีไม่ใช้ pagination)"""
        queryset = Classroom.objects.select_related('school').prefetch_related('teachers', 'students').all()
        if school_id:
            queryset = queryset.filter(school_id=school_id)
        if year:
            queryset = queryset.filter(year=year)
        if number:
            queryset = queryset.filter(number=number)
        return queryset

    @staticmethod
    def create_classroom(data):
        school = data.get('school')
        year = data.get('year')
        number = data.get('number')

        classroom = Classroom.objects.create(
            school=school if isinstance(school, Classroom._meta.get_field('school').remote_field.model) else None,
            school_id=school.id if hasattr(school, 'id') else school,
            year=year,
            number=number
        )
        return classroom

    @staticmethod
    def update_classroom(classroom_instance, data, partial=False):
        if 'school' in data:
            school = data['school']
            classroom_instance.school = school if isinstance(school, Classroom._meta.get_field('school').remote_field.model) else None
            if not isinstance(school, Classroom._meta.get_field('school').remote_field.model):
                classroom_instance.school_id = school
        
        if 'year' in data:
            classroom_instance.year = data['year']
            
        if 'number' in data:
            classroom_instance.number = data['number']

        classroom_instance.save()
        return classroom_instance
    
    @staticmethod
    def delete_classroom(classroom_instance):
        classroom_instance.delete()
        return True

    @staticmethod
    def search_classrooms(school_id=None, year=None, number=None, filters=None, ordering='-id', limit=10, offset=0):
        queryset = Classroom.objects.select_related('school').prefetch_related('teachers', 'students').all()

        if school_id:
            queryset = queryset.filter(school_id=school_id)
        if year:
            queryset = queryset.filter(year=year)
        if number:
            queryset = queryset.filter(number=number)

        if filters and isinstance(filters, dict):
            q_objects = Q()
            for key, val in filters.items():
                if val is not None:
                    q_objects &= Q(**{key: val})
            queryset = queryset.filter(q_objects)

        if ordering:
            queryset = queryset.order_by(ordering)

        total_count = queryset.count()
        classrooms = queryset[offset:offset + limit]

        return classrooms, total_count