from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly

from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from .models import Course

from .serializers import CourseSerializer
# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class=CourseSerializer
    permission_classes=[IsOwnerOrReadOnly,IsAuthenticated]
    queryset=Course.objects.all()
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)