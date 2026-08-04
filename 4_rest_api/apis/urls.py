from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apis.views.v1.school import SchoolHandler
from apis.views.v1.classroom import ClassroomHandler
from apis.views.v1.teacher import TeacherHandler

router = DefaultRouter()
router.register(r'schools', SchoolHandler, basename='school')
router.register(r'classrooms', ClassroomHandler, basename='classroom')
router.register(r'teachers', TeacherHandler, basename='teacher')

api_v1_urls = (router.urls, 'v1')

urlpatterns = [
    path('v1/', include(api_v1_urls))
]