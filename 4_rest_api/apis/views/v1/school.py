from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from apis.services.school_service import SchoolService
from apis.dto.school_dto import SchoolRequestDTO, SchoolResponseDTO


class SchoolHandler(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = SchoolResponseDTO

    def list(self, request):
        name = request.query_params.get('name')
        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))

        schools, total_count = SchoolService.search_schools(
            keyword=name,
            ordering='-id',
            limit=limit,
            offset=offset
        )

        serializer = SchoolResponseDTO(schools, many=True)
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

    def create(self, request):
        serializer = SchoolRequestDTO(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "msg": serializer.errors,
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            school = SchoolService.create_school(serializer.validated_data)
            return Response({
                "status": status.HTTP_201_CREATED,
                "msg": "created successfully",
                "data": SchoolResponseDTO(school).data
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "msg": str(e),
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        school = SchoolService.get_school_by_id(pk)
        if not school:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "msg": "school not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": status.HTTP_200_OK,
            "msg": "success",
            "data": SchoolResponseDTO(school).data
        }, status=status.HTTP_200_OK)

    def update(self, request, pk=None, partial=False):
        school = SchoolService.get_school_by_id(pk)
        if not school:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "msg": "school not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        is_partial = partial or request.method == 'PATCH'
        serializer = SchoolRequestDTO(school, data=request.data, partial=is_partial)
        if not serializer.is_valid():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "msg": serializer.errors,
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        updated_school = SchoolService.update_school(school, serializer.validated_data)
        return Response({
            "status": status.HTTP_200_OK,
            "msg": "updated successfully",
            "data": SchoolResponseDTO(updated_school).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        school = SchoolService.get_school_by_id(pk)
        if not school:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "msg": "school not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        SchoolService.delete_school_by_id(school.id)

        return Response({
            "status": status.HTTP_200_OK,
            "msg": "deleted successfully",
            "data": None
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='search')
    def search_schools(self, request):
        data = request.data or {}
        keyword = data.get('keyword')
        filters = data.get('filter') or data.get('where')
        ordering = data.get('ordering', '-id')
        limit = data.get('limit', 10)
        offset = data.get('offset', 0)

        schools, total_count = SchoolService.search_schools(
            keyword=keyword,
            filters=filters,
            ordering=ordering,
            limit=limit,
            offset=offset
        )

        serializer = SchoolResponseDTO(schools, many=True)
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