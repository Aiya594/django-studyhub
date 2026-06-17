from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from .models import CustomUser
from .serializers import RegisterSerializer,ProfileSerializer

# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]
    queryset = CustomUser.objects.all()
    
    def create(self, request, *args, **kwargs):
        serialzer=self.get_serializer(data=request.data)
        serialzer.is_valid(raise_exception=True)
        user=serialzer.save()
        
        refresh=RefreshToken.for_user(user)
        
        return Response({
            'user': RegisterSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'User regirstered successfully'
        }, status=status.HTTP_201_CREATED)
    
    
class ProfileView(generics.RetrieveAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh=request.data.get('refresh_token')
        if refresh:
            token=RefreshToken(refresh)
            token.blacklist()
            
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception:
        return Response({
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)