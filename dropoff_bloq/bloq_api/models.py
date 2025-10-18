from django.db import models, transaction
import uuid
from bloq_api.enums.rent_size import RentSize
from bloq_api.enums.rent_status import RentStatus
from bloq_api.enums.locker_status import LockerStatus


def enum_to_choices(enum_cls):
    return [(e.name, e.name.title()) for e in enum_cls]

class Rent(models.Model):
    id = models.AutoField(primary_key=True)
    rentId = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    locker = models.ForeignKey(
        "Locker",
        on_delete=models.PROTECT,
        related_name="rents",
        null=True, blank=True
    )
    weight = models.FloatField()
    size = models.CharField(
        max_length=15,
        choices=enum_to_choices(RentSize),
        default=RentSize.M.value,
    )
    status = models.CharField(
        max_length=20,
        choices=enum_to_choices(RentStatus),
        default=RentStatus.CREATED.value,
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Se a rent mudar o status para DELIVERED:
        - libera o locker (isOccupied = False)
        - remove o vínculo (locker = None)
        """
        before_status = None
        before_locker_id = None

        if self.pk:
            try:
                prev = Rent.objects.only("status", "locker_id").get(pk=self.pk)
                before_status = prev.status
                before_locker_id = prev.locker_id
            except Rent.DoesNotExist:
                pass

        became_delivered = (
            before_status != RentStatus.DELIVERED.name and
            self.status == RentStatus.DELIVERED.name
        )

        locker_to_free_id = None
        if became_delivered:
            locker_to_free_id = before_locker_id or self.locker_id
            self.locker = None

        super().save(*args, **kwargs)

        if became_delivered and locker_to_free_id:
            from .models import Locker
            Locker.objects.select_for_update().filter(
                pk=locker_to_free_id, isOccupied=True
            ).update(isOccupied=False)

    def __str__(self):
        return f"Rent {self.rentId} ({self.status})"

class Locker(models.Model):
    id = models.AutoField(primary_key=True)
    lockerId = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    bloq = models.ForeignKey("Bloq", on_delete=models.PROTECT, related_name="lockers")
    status = models.CharField(
        max_length=10,
        choices=enum_to_choices(LockerStatus),
        default=LockerStatus.CLOSED.value,
    )
    isOccupied = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bloq.title} - {self.lockerId}"
    
class Bloq(models.Model):
    id = models.AutoField(primary_key=True)
    bloqId = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
