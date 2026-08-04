from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from apis.models import Student
from apis.serializers import StudentSerializer
from apis.services.student_service import StudentService


class StudentHandler(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
        school_id = request.query_params.get('school_id') or request.query_params.get('school')
        classroom_id = request.query_params.get('classroom_id') or request.query_params.get('classroom')
        name = request.query_params.get('name') or request.query_params.get('keyword')
        gender = request.query_params.get('gender')
        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))

        students, total_count = StudentService.search_students(
            school_id=school_id,
            classroom_id=classroom_id,
            name=name,
            gender=gender,
            ordering='-id',
            limit=limit,
            offset=offset
        )

        serializer = self.get_serializer(students, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "msg": "success",
            "data": {
                "items": serializer.data,
                "item_count": len(serializer.data),
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset
                }
            }
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = StudentService.create_student(serializer.validated_data)
        return Response({
            "status": status.HTTP_201_CREATED,
            "msg": "success",
            "data": self.get_serializer(student).data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        student = StudentService.get_student_by_id(pk)
        if not student:
            return Response({"status": status.HTTP_404_NOT_FOUND, "msg": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(student)
        return Response({
            "status": status.HTTP_200_OK,
            "msg": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        student = StudentService.get_student_by_id(pk)
        if not student:
            return Response({"status": status.HTTP_404_NOT_FOUND, "msg": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(student, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        updated_student = StudentService.update_student(student, serializer.validated_data, partial=kwargs.get('partial', False))

        return Response({
            "status": status.HTTP_200_OK,
            "msg": "success",
            "data": self.get_serializer(updated_student).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        student = StudentService.get_student_by_id(pk)
        if not student:
            return Response({"status": status.HTTP_404_NOT_FOUND, "msg": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        StudentService.delete_student(student)
        return Response({
            "status": status.HTTP_200_OK,
            "msg": "deleted successfully"
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='search')
    def search_students(self, request):
        data = request.data or {}
        school_id = data.get('school_id') or data.get('school')
        classroom_id = data.get('classroom_id') or data.get('classroom')
        name = data.get('name') or data.get('keyword')
        gender = data.get('gender')
        filters = data.get('filter') or data.get('where')
        ordering = data.get('ordering', '-id')
        limit = data.get('limit', 10)
        offset = data.get('offset', 0)

        students, total_count = StudentService.search_students(
            school_id=school_id,
            classroom_id=classroom_id,
            name=name,
            gender=gender,
            filters=filters,
            ordering=ordering,
            limit=limit,
            offset=offset
        )

        serializer = self.get_serializer(students, many=True)
        items_data = serializer.data

        return Response({
            "status": status.HTTP_200_OK,
            "msg": "success",
            "data": {
                "items": items_data,
                "item_count": len(items_data),
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset
                }
            }
        }, status=status.HTTP_200_OK)