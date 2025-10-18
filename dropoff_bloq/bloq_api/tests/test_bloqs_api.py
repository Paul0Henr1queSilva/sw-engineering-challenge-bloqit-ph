import pytest
from .factories import make_bloq, make_locker

pytestmark = pytest.mark.django_db

def test_get_bloq_by_bloqId_returns_lockerIds(auth):
    bloq = make_bloq()
    l1 = make_locker(bloq=bloq)
    l2 = make_locker(bloq=bloq)

    res = auth.get(f"/api/v1/bloqs/{bloq.bloqId}")
    assert res.status_code == 200
    data = res.json()
    assert str(l1.lockerId) in data["lockerIds"]
    assert str(l2.lockerId) in data["lockerIds"]

def test_get_bloq_not_found_with_wrong_uuid(auth):
    res = auth.get("/api/v1/bloqs/00000000-0000-0000-0000-000000000000")
    assert res.status_code == 404
