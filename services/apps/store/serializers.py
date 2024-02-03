from rest_framework import serializers

from services.apps.pets.serializers import PetSerializer
from .models import Order


class StoreSerializer(serializers.ModelSerializer):
    pet = PetSerializer()

    class Meta:
        model = Order
        fields = ['id', 'pet', 'quantity', 'shipDate', 'status', 'complete']

    def create(self, validated_data):
        pet_data = validated_data.pop('pet')
        pet_instance = PetSerializer.create(PetSerializer(), validated_data=pet_data)
        store_instance = Order.objects.create(pet=pet_instance, **validated_data)
        return store_instance

    def update(self, instance, validated_data):
        pet_data = validated_data.pop('pet')
        pet_instance = instance.pet

        PetSerializer.update(PetSerializer(), pet_instance, validated_data=pet_data)

        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.shipDate = validated_data.get('shipDate', instance.shipDate)
        instance.status = validated_data.get('status', instance.status)
        instance.complete = validated_data.get('complete', instance.complete)

        instance.save()

        return instance
