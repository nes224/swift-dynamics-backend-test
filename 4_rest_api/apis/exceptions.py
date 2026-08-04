from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "msg": "Data already exists or violates unique constraint.",
            "errors": {"detail": str(exc)}
        }, status=status.HTTP_400_BAD_REQUEST)


    if response is not None:
        return Response({
            "status": response.status_code,
            "msg": "Invalid input data",
            "errors": response.data
        }, status=response.status_code)

    return response