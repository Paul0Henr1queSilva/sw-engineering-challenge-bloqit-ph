from enum import Enum

class RentStatus(str, Enum):
    CREATED = "created"
    WAITING_DROPOFF = "waiting_dropoff"
    WAITING_PICKUP = "waiting_pickup"
    DELIVERED = "delivered"