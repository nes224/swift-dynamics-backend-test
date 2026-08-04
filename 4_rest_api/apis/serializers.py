from rest_framework import serializers
from .models import School, Classroom, Teacher, Student

class SchoolSerializer(serializers.ModelSerializer):
    classroom_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = ['id', 'name', 'short_name', 'address', 'classroom_count', 'teacher_count', 'student_count']

    def get_classroom_count(self, obj):
        return obj.classrooms.count()

    def get_teacher_count(self, obj):
        return Teacher.objects.filter(classrooms__school=obj).distinct().count()

    def get_student_count(self, obj):
        return Student.objects.filter(classroom__school=obj).count()

class TeacherInClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender']

class StudentInClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender']
class ClassroomSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    teachers = TeacherInClassroomSerializer(many=True, read_only=True)
    students = StudentInClassroomSerializer(many=True, read_only=True)
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = [
            'id', 
            'school', 
            'school_name', 
            'year', 
            'number', 
            'teachers', 
            'students', 
            'teacher_count', 
            'student_count'
        ]

    def get_teacher_count(self, obj):
        return obj.teachers.count()

    def get_student_count(self, obj):
        return obj.students.count()

class ClassroomInTeacherSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'year', 'number', 'school', 'school_name']
class TeacherSerializer(serializers.ModelSerializer):
    classrooms_info = ClassroomInTeacherSerializer(source='classrooms', many=True, read_only=True)
    classroom_count = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender', 'classrooms', 'classrooms_info', 'classroom_count']

    def get_classroom_count(self, obj):
        return obj.classrooms.count()

class StudentSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='classroom.school.name', read_only=True)
    classroom_info = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'classroom', 'school_name', 'classroom_info']

    def get_classroom_info(self, obj):
        if obj.classroom:
            return f"ม.{obj.classroom.year}/{obj.classroom.number}"
        return None

