from rest_framework import serializers
from apis.models import School

class SchoolRequestDTO(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['name', 'short_name', 'address']
class SchoolResponseDTO(serializers.ModelSerializer):
    classroom_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = [
            'id', 
            'name', 
            'short_name', 
            'address', 
            'classroom_count', 
            'teacher_count', 
            'student_count'
        ]

    def get_classroom_count(self, obj) -> int:
        return obj.classrooms.count() if hasattr(obj, 'classrooms') else 0

    def get_teacher_count(self, obj) -> int:
        from apis.models import Teacher
        return Teacher.objects.filter(classrooms__school=obj).distinct().count()

    def get_student_count(self, obj) -> int:
        from apis.models import Student
        return Student.objects.filter(classroom__school=obj).count()