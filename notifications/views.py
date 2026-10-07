from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    notifications = Notification.objects.filter(user_id=request.user.id)
    data = [
        {"id": n.id, "message": n.message, "created_at": n.created_at}
        for n in notifications
    ]
    return Response(data)
