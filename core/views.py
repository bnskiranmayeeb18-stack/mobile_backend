from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from.models import DriverLocation

# 1. REGISTER - kotha user create chestundi
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({"error": "username and password required"}, status=400)

    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "message": "User already exists"})

    user = User.objects.create_user(username=username, password=password, email=email)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "username": user.username})

# 2. LOGIN - token istundi
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response({"error": "Invalid credentials"}, status=400)

# 3. UPDATE DRIVER LOCATION - nee main task
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_driver_location(request):
    lat = request.data.get('latitude')
    lng = request.data.get('longitude')

    if lat is None or lng is None:
        return Response({"error": "latitude and longitude required"}, status=400)

    try:
        lat = float(lat)
        lng = float(lng)
    except:
        return Response({"error": "Invalid latitude/longitude"}, status=400)

    # Save or update
    obj, created = DriverLocation.objects.update_or_create(
        driver=request.user,
        defaults={'latitude': lat, 'longitude': lng}
    )
    return Response({
        "message": "Location updated",
        "driver": request.user.username,
        "latitude": obj.latitude,
        "longitude": obj.longitude
    }, status=200)