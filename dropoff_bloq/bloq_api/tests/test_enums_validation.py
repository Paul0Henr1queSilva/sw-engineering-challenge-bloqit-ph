import pytest
from .factories import make_locker

pytestmark = pytest.mark.django_db

def test_rent_rejects_invalid_status(auth):
    locker = make_locker()
    payload = {"lockerId": str(locker.lockerId), "weight": 1, "size": "medium", "status": "INVALID"}
    res = auth.post("/api/v1/rents", payload, format="json")
    assert res.status_code == 400
    assert "status" in res.json()

def test_rent_rejects_invalid_size(auth):
    locker = make_locker()
    payload = {"lockerId": str(locker.lockerId), "weight": 1, "size": "mega", "status": "created"}
    res = auth.post("/api/v1/rents", payload, format="json")
    assert res.status_code == 400
    assert "size" in res.json()
