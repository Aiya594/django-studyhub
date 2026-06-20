from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    CourseViewSet,
    LessonViewSet,
    EnrollmentListCreateView,
    EnrollmentDestroyView,
)


router = DefaultRouter()
router.register(
    r"courses",
    CourseViewSet,
    basename="course"
)

router.register(
    r"courses/(?P<course_id>\d+)/lessons",
    LessonViewSet,
    basename="course-lessons"
)


urlpatterns = [
    path(
        "enrollments/",
        EnrollmentListCreateView.as_view(),
        name="enrollment-list-create"
    ),
    path(
        "enrollments/<int:pk>/",
        EnrollmentDestroyView.as_view(),
        name="enrollment-delete"
    ),
]

urlpatterns += router.urls