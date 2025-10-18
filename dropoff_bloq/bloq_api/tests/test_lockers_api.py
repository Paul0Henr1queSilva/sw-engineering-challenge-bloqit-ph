import pytest
from .factories import make_bloq, make_locker, make_rent

pytestmark = pytest.mark.django_db

def test_list_lockers_returns_rentId_when_exists(auth):
    bloq = make_bloq()
    locker = make_locker(bloq=bloq, isOccupied=True)
    rent = make_rent(locker=locker, status="WAITING_DROPOFF")

    res = auth.get("/api/v1/lockers")
    assert res.status_code == 200
    body = res.json()
    row = next(i for i in (body.get("results") or body) if i["lockerId"] == str(locker.lockerId))
    assert row["rentId"] == str(rent.rentId)

def test_create_locker_with_bloqId(auth):
    bloq = make_bloq()
    payload = {"bloqId": str(bloq.bloqId), "status": "CLOSED", "isOccupied": False}
    res = auth.post("/api/v1/lockers", payload, format="json")
    assert res.status_code == 201, res.content
    data = res.json()
    assert data["bloqId"] == str(bloq.bloqId)
    assert data["status"] == "CLOSED"

def test_patch_locker_does_not_require_bloqId(auth):
    locker = make_locker(status="CLOSED")
    res = auth.patch(f"/api/v1/lockers/{locker.lockerId}", {"status": "OPEN"}, format="json")
    assert res.status_code == 200, res.content
    assert res.json()["status"] == "OPEN"

def test_get_locker_by_lockerId(auth):
    locker = make_locker()
    res = auth.get(f"/api/v1/lockers/{locker.lockerId}")
    assert res.status_code == 200
    assert res.json()["lockerId"] == str(locker.lockerId)
