from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apis.models import Classroom
from apis.serializers import ClassroomSerializer
from apis.services.classroom_service import ClassroomService


class ClassroomHandler(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    def list(self, request, *args, **kwargs):
        school_id = request.query_params.get('school_id') or request.query_params.get('school')
        year = request.query_params.get('year')
        number = request.query_params.get('number')
        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))

        classrooms, total_count = ClassroomService.search_classrooms(
            school_id=school_id,
            year=year,
            number=number,
            ordering='-id',
            limit=limit,
            offset=offset
        )

        serializer = self.get_serializer(classrooms, many=True)
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
        classroom = serializer.save()
        if not serializer.is_valid():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "msg": "Classroom with this year and number already exists in this school." 
                       if "non_field_errors" in serializer.errors else "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            classroom = ClassroomService.create_classroom(serializer.validated_data)
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "msg": "Classroom with this year and number already exists in this school."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": status.HTTP_201_CREATED,
            "msg": "success",
            "data": self.get_serializer(classroom).data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        classroom = ClassroomService.get_classroom_by_id(pk)
        if not classroom:
            return Response({"status": status.HTTP_404_NOT_FOUND, "msg": "Classroom not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(classroom)
        return Response({
            "status": status.HTTP_200_OK,
            "msg": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        classroom = ClassroomService.get_classroom_by_id(pk)
        if not classroom:
            return Response({"status": status.HTTP_404_NOT_FOUND, "msg": "Classroom not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(classroom, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        updated_classroom = serializer.save()

        return Response({
            "status": status.HTTP_200_OK,
            "msg": "success",
            "data": self.get_serializer(updated_classroom).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        classroom = ClassroomService.get_classroom_by_id(pk)
        if not classroom:
            return Response({"status": status.HTTP_404_NOT_FOUND, "msg": "Classroom not found"}, status=status.HTTP_404_NOT_FOUND)

        classroom.delete()
        return Response({
            "status": status.HTTP_200_OK,
            "msg": "deleted successfully"
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='search')
    def search_classrooms(self, request):
        data = request.data or {}
        school_id = data.get('school_id') or data.get('school')
        year = data.get('year')
        number = data.get('number')
        filters = data.get('filter') or data.get('where')
        ordering = data.get('ordering', '-id')
        limit = data.get('limit', 10)
        offset = data.get('offset', 0)

        classrooms, total_count = ClassroomService.search_classrooms(
            school_id=school_id,
            year=year,
            number=number,
            filters=filters,
            ordering=ordering,
            limit=limit,
            offset=offset
        )

        serializer = self.get_serializer(classrooms, many=True)
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