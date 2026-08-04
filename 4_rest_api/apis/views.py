from rest_framework import viewsets
from .models import School, Classroom, Teacher, Student
from .serializers import (
    SchoolSerializer, 
    ClassroomSerializer, 
    TeacherSerializer, 
    StudentSerializer
)

class SchoolHandler(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class ClassroomHandler(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class TeacherHandler(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentHandler(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer