from rest_framework.test import APIClient
import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def auth(db):
  User = get_user_model()
  user = User.objects.create_user("tester", password="pass")
  api = APIClient()
  api.force_authenticate(user=user)
  return api