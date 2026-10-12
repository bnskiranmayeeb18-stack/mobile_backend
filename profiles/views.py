from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

class ProfileImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('image')
        if not file:
            return Response({"success":False,"message":"Missing file","error_code":"MISSING_FILE"}, status=400)
        if file.content_type not in ['image/jpeg','image/png']:
            return Response({"success":False,"message":"Invalid file type","error_code":"INVALID_TYPE"}, status=400)
        if file.size > 2*1024*1024:
            return Response({"success":False,"message":"File too large max 2MB","error_code":"FILE_TOO_LARGE"}, status=400)

        profile = request.user.profile
        profile.image.save(file.name, file)
        return Response({"success":True,"data":{"image_url": profile.image.url}})