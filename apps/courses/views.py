from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly

from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Course,Lesson

from .serializers import CourseSerializer,LessonSerializer
# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class=CourseSerializer
    permission_classes=[IsOwnerOrReadOnly,IsAuthenticated]
    queryset=Course.objects.all()
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
    
    
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class=LessonSerializer
    permission_classes=[IsAuthenticated]
    queryset=Lesson.objects.all()

    
    def perform_create(self,serializer):
        course = get_object_or_404(
            Course,
            id=self.kwargs['course_id'],
            owner=self.request.user)
        return serializer.save(course=course)
    
    def get_queryset(self):
        return Lesson.objects.filter(
            course_id=self.kwargs['course_id'],
            course__owner=self.request.user)
 