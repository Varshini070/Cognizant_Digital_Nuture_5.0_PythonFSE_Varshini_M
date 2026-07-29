from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, DepartmentViewSet, EnrollmentViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
]
