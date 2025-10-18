from rest_framework import serializers
from django.db import transaction
from ..models import Rent, Locker, Bloq
from bloq_api.enums.rent_status import RentStatus


class RentSerializer(serializers.ModelSerializer):
    lockerId = serializers.SlugRelatedField(
        source="locker",
        slug_field="lockerId",
        queryset=Locker.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Rent
        fields = [
            "id", "rentId", "lockerId",
            "weight", "size", "status",
            "createdAt", "updatedAt",
        ]
        read_only_fields = ["rentId", "createdAt", "updatedAt"]

    def validate(self, attrs):
        locker = attrs.get("locker", getattr(self.instance, "locker", None))
        # caso esteja setando um novo locker (ou trocando)
        if "locker" in attrs and locker is not None:
            if locker.isOccupied:
                raise serializers.ValidationError({"lockerId": "Este locker já está ocupado."})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        locker = validated_data.get("locker")
        rent = super().create(validated_data)
        if locker is not None and not locker.isOccupied:
            # opcional: travar a linha p/ concorrência alta
            locker = Locker.objects.select_for_update().get(pk=locker.pk)
            if locker.isOccupied:
                raise serializers.ValidationError({"lockerId": "Este locker já está ocupado."})
            locker.isOccupied = True
            locker.save(update_fields=["isOccupied"])
        return rent
    
    @transaction.atomic
    def update(self, instance, validated_data):
        old_locker = instance.locker
        new_locker = validated_data.get("locker", old_locker)

        rent = super().update(instance, validated_data)

        if old_locker and new_locker and old_locker.pk != new_locker.pk:
            
            ol = Locker.objects.select_for_update().get(pk=old_locker.pk)
            ol.isOccupied = False
            ol.save(update_fields=["isOccupied"])
           
            nl = Locker.objects.select_for_update().get(pk=new_locker.pk)
            if nl.isOccupied:
                raise serializers.ValidationError({"lockerId": "Locker de destino já está ocupado."})
            nl.isOccupied = True
            nl.save(update_fields=["isOccupied"])

        
        elif old_locker is None and new_locker is not None:
            nl = Locker.objects.select_for_update().get(pk=new_locker.pk)
            if nl.isOccupied:
                raise serializers.ValidationError({"lockerId": "Este locker já está ocupado."})
            nl.isOccupied = True
            nl.save(update_fields=["isOccupied"])

        elif old_locker is not None and new_locker is None:
            ol = Locker.objects.select_for_update().get(pk=old_locker.pk)
            ol.isOccupied = False
            ol.save(update_fields=["isOccupied"])

        if rent.status == RentStatus.DELIVERED.value:
            target = new_locker or old_locker
            if target:
                locker = Locker.objects.select_for_update().get(pk=target.pk)
                if locker.isOccupied:
                    locker.isOccupied = False
                    locker.save(update_fields=["isOccupied"])
     
            rent.locker = None
            rent.save(update_fields=["locker"])

        return rent
    

class BloqSerializer(serializers.ModelSerializer):
    lockerIds = serializers.SerializerMethodField()

    class Meta:
        model = Bloq
        fields = ["bloqId", "title", "address", "lockerIds", "createdAt", "updatedAt"]
        read_only_fields = ["bloqId", "createdAt", "updatedAt"]

    def get_lockerIds(self, obj):
        
        return list(obj.lockers.values_list("lockerId", flat=True))


class LockerSerializer(serializers.ModelSerializer):
    bloqId = serializers.SlugRelatedField(
        source="bloq",
        slug_field="bloqId",
        queryset=Bloq.objects.all(),
        required=False,
        allow_null=False
    )

    rentId = serializers.SerializerMethodField() 

    class Meta:
        model = Locker
        fields = ["lockerId", "bloqId", "rentId","status", "isOccupied", "createdAt", "updatedAt"]
        read_only_fields = ["lockerId", "createdAt", "updatedAt"]

    def get_rentId(self, obj):
        rent = obj.rents.order_by("-createdAt").first()
        if rent:
            return str(rent.rentId)
        return None


