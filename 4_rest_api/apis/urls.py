from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apis.views.v1.school import SchoolHandler

router = DefaultRouter()
router.register(r'schools', SchoolHandler, basename='school')

api_v1_urls = (router.urls, 'v1')

urlpatterns = [
    path('v1/', include(api_v1_urls))
]