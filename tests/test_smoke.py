import pytest

def test_smoke():
    assert 1 + 1 == 2

@pytest.mark.django_db
def test_django_settings():
    from django.conf import settings
    assert settings.BASE_DIR.exists()
