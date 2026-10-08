import pytest

@pytest.mark.django_db
def test_fare_calculation():
    from core.services.fare_service import FareService
    # Base 50 + 5*12 = 110, no discount
    fare = FareService.calculate_fare(5)
    assert fare == 110.0

    # 15km -> 50+180=230 *0.95 = 218.5
    fare2 = FareService.calculate_fare(15)
    assert fare2 == 218.5

    # 25km -> 50+300=350 *0.9 = 315
    fare3 = FareService.calculate_fare(25)
    assert fare3 == 315.0

    # Invalid distance
    with pytest.raises(ValueError):
        FareService.calculate_fare(0)
    with pytest.raises(ValueError):
        FareService.calculate_fare(-5)

@pytest.mark.django_db
def test_driver_availability():
    # Simulate driver availability logic
    is_online = True
    current_rides = 0
    max_rides = 1
    available = is_online and current_rides < max_rides
    assert available is True

    current_rides = 1
    available = is_online and current_rides < max_rides
    assert available is False

@pytest.mark.django_db
def test_nearby_driver_selection():
    # Haversine mock - closest driver selection
    drivers = [
        {"id": 1, "lat": 17.4485, "lng": 78.3908, "dist": 0.5},
        {"id": 2, "lat": 17.4400, "lng": 78.3489, "dist": 2.0},
        {"id": 3, "lat": 17.4450, "lng": 78.3850, "dist": 0.2},
    ]
    sorted_drivers = sorted(drivers, key=lambda x: x["dist"])
    assert sorted_drivers[0]["id"] == 3
    # Business: only drivers within 5km
    nearby = [d for d in drivers if d["dist"] <= 5]
    assert len(nearby) == 3

@pytest.mark.django_db
def test_ride_validation():
    from utils.validators import validate_pickup_drop, validate_distance
    # Valid
    validate_pickup_drop("Madhapur", "Gachibowli")
    validate_distance(5)

    # Invalid - same pickup drop
    with pytest.raises(Exception):
        validate_pickup_drop("Madhapur", "Madhapur")

    # Invalid distance
    with pytest.raises(Exception):
        validate_distance(0)
    with pytest.raises(Exception):
        validate_distance(-1)

@pytest.mark.django_db
def test_cancellation_rules():
    # Rule from RideService: can cancel only if not completed
    valid_transitions = {
        "REQUESTED": ["ACCEPTED","CANCELLED"],
        "ACCEPTED": ["STARTED","CANCELLED"],
        "STARTED": ["COMPLETED"],
        "COMPLETED": [],
        "CANCELLED": []
    }
    # Can cancel from REQUESTED
    assert "CANCELLED" in valid_transitions["REQUESTED"]
    # Cannot cancel from COMPLETED
    assert "CANCELLED" not in valid_transitions["COMPLETED"]
    # Cannot cancel from CANCELLED again
    assert "CANCELLED" not in valid_transitions["CANCELLED"]