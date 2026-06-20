from rest_framework.routers import DefaultRouter
from .views import CourseViewSet,LessonViewSet

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


urlpatterns = router.urls