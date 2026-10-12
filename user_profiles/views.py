from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from core.response import standard_response
from.models import UserProfile
import os

ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
MAX_SIZE = 5 * 1024 * 1024 # 5MB
ALLOWED_EXTS = ['jpg','jpeg','png','webp']

class ProfileImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # Task 3 Validation: Missing file
        file_obj = request.FILES.get('image') or request.FILES.get('profile_image') or request.FILES.get('file')

        if not file_obj:
            return standard_response(success=False, message="No image file provided", error_code="NO_FILE", status_code=400)

        # Validate: Filename
        if not file_obj.name or '.' not in file_obj.name:
            return standard_response(success=False, message="Invalid filename", error_code="INVALID_FILENAME", status_code=400)

        ext = file_obj.name.split('.')[-1].lower()
        if ext not in ALLOWED_EXTS:
            return standard_response(success=False, message=f"Invalid file type. Allowed: {ALLOWED_EXTS}", error_code="INVALID_FILE_TYPE", status_code=400)

        # Validate: File type MIME
        if file_obj.content_type not in ALLOWED_TYPES:
            return standard_response(success=False, message="Invalid file type. Only JPEG, PNG, WEBP allowed", error_code="INVALID_FILE_TYPE", status_code=400)

        # Validate: File size
        if file_obj.size > MAX_SIZE:
            return standard_response(success=False, message="File too large. Max 5MB", error_code="FILE_TOO_LARGE", status_code=400)

        if file_obj.size == 0:
            return standard_response(success=False, message="Invalid file - empty file", error_code="INVALID_FILE", status_code=400)

        # Save
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.image = file_obj
        profile.save()

        return standard_response(success=True, message="Profile image uploaded successfully", data={"image_url": profile.image.url, "filename": file_obj.name})

# Also add GET for current profile
from rest_framework.decorators import api_view, permission_classes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    from.serializers import UserProfileSerializer
    data = UserProfileSerializer(profile).data if hasattr(__import__('user_profiles.serializers', fromlist=['UserProfileSerializer']), 'UserProfileSerializer') else {"image": profile.image.url if profile.image else None, "bio": profile.bio}
    return standard_response(success=True, message="Profile fetched", data=data)
