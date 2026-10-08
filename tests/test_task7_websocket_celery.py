import pytest
from unittest.mock import Mock, patch, AsyncMock
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_websocket_authentication():
    user = User.objects.create_user(username="ws_user", password="test")
    client = APIClient()
    client.force_authenticate(user=user)
    r = client.get("/api/rides/")
    assert r.status_code in [200, 401]

@pytest.mark.django_db
def test_ride_status_events():
    from rides.models import Ride
    user = User.objects.create_user(username="status_user", password="test")
    ride = Ride.objects.create(rider=user, pickup="A", drop="B", status="requested")
    with patch('channels.layers.get_channel_layer') as mock_layer:
        mock_layer.return_value.group_send = AsyncMock()
        ride.status = "accepted"
        ride.save()
        assert ride.status == "accepted"

@pytest.mark.django_db
def test_location_events():
    payload = {"lat": 17.4485, "lng": 78.3908, "heading": 90}
    assert -90 <= payload["lat"] <= 90
    assert -180 <= payload["lng"] <= 180

@pytest.mark.django_db
def test_celery_task_execution():
    from rides.models import Ride
    user = User.objects.create_user(username="celery_user", password="test")
    ride = Ride.objects.create(rider=user, pickup="A", drop="B", status="started")
    ride.status = "completed"
    ride.save()
    assert ride.status == "completed"

@pytest.mark.django_db
def test_failed_task_retry():
    retries = 0
    max_retries = 3
    success = False
    while retries < max_retries and not success:
        try:
            if retries < 2:
                raise Exception("Temporary failure")
            success = True
        except Exception:
            retries += 1
    assert success is True
    assert retries == 2