from .views import * 
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", logout_view, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]