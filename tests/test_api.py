import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rides.models import Ride
import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: f'testuser{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@test.com')

class RideFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ride
    rider = factory.SubFactory(UserFactory)
    pickup = "Ameerpet"
    drop = "Gachibowli"
    status = "requested"

@pytest.mark.django_db
def test_health_check():
    client = APIClient()
    response = client.get('/api/core/health/')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

@pytest.mark.django_db
def test_jwt_token_invalid_should_fail():
    client = APIClient()
    response = client.post('/api/auth/token/', {'username': 'fake', 'password': 'fake123'}, format='json')
    assert response.status_code in [401, 400]

@pytest.mark.django_db
def test_jwt_token_valid_flow():
    User.objects.create_user(username='jwtuser', password='pass12345')
    client = APIClient()
    response = client.post('/api/auth/token/', {'username': 'jwtuser', 'password': 'pass12345'}, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_rides_list_requires_auth():
    client = APIClient()
    response = client.get('/api/rides/')
    assert response.status_code == 401

@pytest.mark.django_db
def test_rides_crud_with_factory_and_fixture():
    user = UserFactory(username='rider1')
    user.set_password('testpass123')
    user.save()

    client = APIClient()
    token_resp = client.post('/api/auth/token/', {'username': 'rider1', 'password': 'testpass123'}, format='json')
    access = token_resp.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    # FIXED: use pickup/drop as per model
    resp = client.post('/api/rides/create/', {'pickup': 'Rajahmundry', 'drop': 'Vijayawada'}, format='json')
    assert resp.status_code == 201, resp.data

    resp = client.get('/api/rides/')
    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert resp.data[0]['pickup'] == 'Rajahmundry'

@pytest.mark.django_db
@patch('rides.views.RideSerializer')
def test_mocking_example(mock_serializer):
    mock_instance = MagicMock()
    mock_instance.data = [{'id': 1, 'pickup': 'Mocked'}]
    mock_serializer.return_value = mock_instance
    mock_instance.is_valid.return_value = True
    assert mock_serializer is not None
