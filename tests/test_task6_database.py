import pytest
from django.db import IntegrityError
from django.contrib.auth.models import User
from rides.models import Ride
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_model_constraints():
    user = User.objects.create_user(username="constraint_user", password="test")
    # Test that model without rider fails validation via full_clean
    ride = Ride(rider=None, pickup="A", drop="B")
    with pytest.raises(Exception):
        ride.full_clean()  # should raise ValidationError for rider required
        ride.save()

    # Also test empty pickup should fail if blank=False logic enforced in serializer
    ride2 = Ride(rider=user, pickup="", drop="B")
    # serializer level will catch, model allows blank but business rule should catch
    assert ride2.pickup == "" # model allows, but API serializer will reject
    # So we test API rejects
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=user)
    r = client.post("/api/rides/create/", {"pickup":"","drop":"B"}, format='json')
    assert r.status_code == 400

@pytest.mark.django_db
def test_unique_fields():
    User.objects.create_user(username="unique_user_db", password="test")
    with pytest.raises(IntegrityError):
        User.objects.create_user(username="unique_user_db", password="test2")

@pytest.mark.django_db
def test_foreign_keys():
    user = User.objects.create_user(username="fk_user_db", password="test")
    ride = Ride.objects.create(rider=user, pickup="A", drop="B")
    assert ride.rider_id == user.id
    assert ride.rider.username == "fk_user_db"

    # Valid FK check - delete user cascades
    # For invalid FK, SQLite defers check, so we test via get_or_create fails
    from django.db import connection
    # Instead of creating invalid id, test that ride without rider raises
    with pytest.raises(Exception):
        # This will raise IntegrityError at DB level when null rider
        Ride.objects.create(rider=None, pickup="A", drop="B")

@pytest.mark.django_db
def test_required_fields():
    user = User.objects.create_user(username="req_user_db", password="test")
    # Test via serializer - required fields validation
    from rest_framework.test import APIClient
    from rides.serializers import RideSerializer

    # Missing drop
    serializer = RideSerializer(data={"pickup":"A"})
    assert not serializer.is_valid()
    assert "drop" in serializer.errors

    # Missing pickup
    serializer2 = RideSerializer(data={"drop":"B"})
    assert not serializer2.is_valid()
    assert "pickup" in serializer2.errors

    # API level
    client = APIClient()
    client.force_authenticate(user=user)
    r = client.post("/api/rides/create/", {"pickup":"A"}, format='json')
    assert r.status_code == 400
    assert "drop" in str(r.data).lower()

@pytest.mark.django_db
def test_invalid_relationships():
    user = User.objects.create_user(username="rel_user_db", password="test")
    ride = Ride.objects.create(rider=user, pickup="A", drop="B")
    assert ride.rider is not None

    # After user delete, rides should cascade delete (CASCADE)
    user_id = user.id
    user.delete()
    assert not Ride.objects.filter(rider_id=user_id).exists()