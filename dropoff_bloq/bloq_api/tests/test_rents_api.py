import pytest
from django.db import transaction
from .factories import make_bloq, make_locker, make_rent

pytestmark = pytest.mark.django_db

def test_create_rent_with_locker_occupies_it(auth):
    locker = make_locker(isOccupied=False, status="CLOSED")
    payload = {
        "lockerId": str(locker.lockerId),
        "weight": 2.5,
        "size": "M",
        "status": "CREATED",
    }
    res = auth.post("/api/v1/rents", payload, format="json")
    assert res.status_code == 201, res.content

    # locker deve ficar ocupado
    locker.refresh_from_db()
    assert locker.isOccupied is True

def test_patch_rent_assigns_locker_when_null(auth):
    # cria rent sem locker
    rent = make_rent(locker=None, status="CREATED")
    locker = make_locker(isOccupied=False)

    res = auth.patch(f"/api/v1/rents/{rent.rentId}", {"lockerId": str(locker.lockerId)}, format="json")
    assert res.status_code == 200, res.content

    locker.refresh_from_db()
    assert locker.isOccupied is True

def test_patch_rent_delivered_frees_locker(auth):
    locker = make_locker(isOccupied=True)
    rent = make_rent(locker=locker, status="WAITING_PICKUP")

    res = auth.patch(f"/api/v1/rents/{rent.rentId}", {"status": "DELIVERED"}, format="json")
    assert res.status_code == 200, res.content

    locker.refresh_from_db()
    assert locker.isOccupied is False

def test_get_rent_by_rentId(auth):
    rent = make_rent()
    res = auth.get(f"/api/v1/rents/{rent.rentId}")
    assert res.status_code == 200
    assert res.json()["rentId"] == str(rent.rentId)
