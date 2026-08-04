from django.db.models import Q
from apis.models import Teacher


class TeacherService:

    @staticmethod
    def get_teacher_by_id(teacher_id):
        try:
            return Teacher.objects.prefetch_related('classrooms', 'classrooms__school').get(id=teacher_id)
        except Teacher.DoesNotExist:
            return None

    @staticmethod
    def create_teacher(data):
        classrooms = data.pop('classrooms', [])
        teacher = Teacher.objects.create(**data)
        if classrooms:
            teacher.classrooms.set(classrooms)
        return teacher

    @staticmethod
    def update_teacher(teacher_instance, data, partial=False):
        classrooms = data.pop('classrooms', None)
        
        for attr, value in data.items():
            setattr(teacher_instance, attr, value)
        teacher_instance.save()

        if classrooms is not None:
            teacher_instance.classrooms.set(classrooms)

        return teacher_instance

    @staticmethod
    def delete_teacher(teacher_instance):
        teacher_instance.delete()
        return True

    @staticmethod
    def search_teachers(school_id=None, classroom_id=None, name=None, gender=None, filters=None, ordering='-id', limit=10, offset=0):
        queryset = Teacher.objects.prefetch_related('classrooms', 'classrooms__school').all()

        if school_id:
            queryset = queryset.filter(classrooms__school_id=school_id).distinct()
        if classroom_id:
            queryset = queryset.filter(classrooms__id=classroom_id).distinct()
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
        teachers = queryset[offset:offset + limit]

        return teachers, total_count