import uuid
from model_bakery import baker
from bloq_api.models import Bloq, Locker, Rent

def make_bloq(**kwargs) -> Bloq:
    defaults = dict(title="Bloq Center", address="Rua A, 100")
    defaults.update(kwargs)
    return baker.make(Bloq, **defaults)

def make_locker(**kwargs) -> Locker:
    b = kwargs.pop("bloq", None) or make_bloq()
    defaults = dict(bloq=b, status="CLOSED", isOccupied=False)
    defaults.update(kwargs)
    return baker.make(Locker, **defaults)

def make_rent(**kwargs) -> Rent:
    defaults = dict(weight=1.0, size="M", status="CREATED")
    defaults.update(kwargs)
    return baker.make(Rent, **defaults)
