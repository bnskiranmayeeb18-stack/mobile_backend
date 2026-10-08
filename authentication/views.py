from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import logging

auth_log = logging.getLogger('auth')
api_log = logging.getLogger('api')
User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            name = request.data.get('name', '')
            if not email or not password:
                auth_log.warning(f"REGISTER_FAILED email={email} reason=missing_fields ip={request.META.get('REMOTE_ADDR')}")
                return Response({"error": "Email and password required"}, status=400)
            if User.objects.filter(email=email).exists():
                auth_log.warning(f"REGISTER_FAILED email={email} reason=already_exists")
                return Response({"error": "User already exists"}, status=400)
            user = User.objects.create_user(email=email, password=password, username=email)
            auth_log.info(f"REGISTER_SUCCESS email={email} user_id={user.id}")
            api_log.info(f"API_REQUEST path=/api/auth/register/ method=POST user_id={user.id} status=201")
            return Response({"message": "User registered", "user_id": user.id}, status=201)
        except Exception as e:
            api_log.error(f"API_ERROR path=/api/auth/register/ error={str(e)}")
            return Response({"error": str(e)}, status=500)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password:
                auth_log.warning(f"LOGIN_FAILED email={email} ip={request.META.get('REMOTE_ADDR')} reason=missing_fields")
                return Response({"error": "Email and password required"}, status=400)
            user = authenticate(request, username=email, password=password)
            if not user:
                try:
                    u = User.objects.get(email=email)
                    if u.check_password(password):
                        user = u
                except:
                    pass
            if not user:
                auth_log.warning(f"LOGIN_FAILED email={email} ip={request.META.get('REMOTE_ADDR')} reason=wrong_password")
                return Response({"error": "Invalid credentials"}, status=401)
            refresh = RefreshToken.for_user(user)
            auth_log.info(f"LOGIN_SUCCESS email={email} user_id={user.id} ip={request.META.get('REMOTE_ADDR')}")
            return Response({"access": str(refresh.access_token), "refresh": str(refresh), "user_id": user.id})
        except Exception as e:
            api_log.error(f"API_ERROR path=/api/auth/login/ error={str(e)}")
            return Response({"error": str(e)}, status=500)