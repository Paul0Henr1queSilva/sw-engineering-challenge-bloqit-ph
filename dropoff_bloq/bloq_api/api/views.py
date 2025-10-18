from rest_framework import viewsets, permissions
from ..models import Rent, Locker, Bloq
from .serializers import RentSerializer, LockerSerializer, BloqSerializer

UUID_REGEX = r"[0-9a-f-]{36}" 

class DefaultPermission(permissions.IsAuthenticated):
    pass

class BloqViewSet(viewsets.ModelViewSet):
    queryset = Bloq.objects.all().order_by("-createdAt")
    permission_classes = [permissions.AllowAny]
    serializer_class = BloqSerializer
    lookup_field = "bloqId"
    lookup_value_regex = UUID_REGEX

class LockerViewSet(viewsets.ModelViewSet):
    queryset = Locker.objects.all().order_by("-createdAt")
    permission_classes = [permissions.AllowAny]
    serializer_class = LockerSerializer
    lookup_field = "lockerId"
    lookup_value_regex = UUID_REGEX
    

class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.select_related("locker").all().order_by("-createdAt")
    serializer_class = RentSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "rentId"
    lookup_value_regex = UUID_REGEX