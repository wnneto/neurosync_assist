# === auth_views.py ===
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from rest_framework.permissions import AllowAny
from users.serializers import (
    CustomRegisterSerializer, LoginSerializer,
    UserProfileSerializer,
)



class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    
class CustomLoginView(LoginView):
    serializer_class = LoginSerializer


# === profile_views.py ===
from rest_framework import generics, permissions
from users.models import CustomUser


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
