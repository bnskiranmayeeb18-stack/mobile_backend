from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    if not username or not password:
        return Response({"error": "username, password required"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"error": "User exists"}, status=400)
    if email and User.objects.filter(email=email).exists():
        return Response({"error": "Email exists"}, status=400)
    User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "User created"}, status=201)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair_alt'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_view, name='register'),
]