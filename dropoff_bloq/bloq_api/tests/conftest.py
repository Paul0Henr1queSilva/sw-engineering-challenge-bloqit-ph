import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

@pytest.fixture
def api():
    return APIClient()

@pytest.fixture
@pytest.mark.django_db
def user():
    User = get_user_model()
    return User.objects.create_user(username="tester", password="pass")

@pytest.fixture
def auth(api, user):
    api.force_authenticate(user=user)
    return api
