from django.db.models import Q
from apis.models import Student


class StudentService:

    @staticmethod
    def get_student_by_id(student_id):
        try:
            return Student.objects.select_related('classroom', 'classroom__school').get(id=student_id)
        except Student.DoesNotExist:
            return None

    @staticmethod
    def create_student(data):
        return Student.objects.create(**data)

    @staticmethod
    def update_student(student_instance, data, partial=False):
        for attr, value in data.items():
            setattr(student_instance, attr, value)
        student_instance.save()
        return student_instance

    @staticmethod
    def delete_student(student_instance):
        student_instance.delete()
        return True

    @staticmethod
    def search_students(school_id=None, classroom_id=None, name=None, gender=None, filters=None, ordering='-id', limit=10, offset=0):
        queryset = Student.objects.select_related('classroom', 'classroom__school').all()

        if school_id:
            queryset = queryset.filter(classroom__school_id=school_id)
        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        if gender:
            queryset = queryset.filter(gender=gender)
        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            )

        if filters and isinstance(filters, dict):
            q_objects = Q()
            for key, val in filters.items():
                if val is not None:
                    q_objects &= Q(**{key: val})
            queryset = queryset.filter(q_objects)

        if ordering:
            queryset = queryset.order_by(ordering)

        total_count = queryset.count()
        students = queryset[offset:offset + limit]

        return students, total_count