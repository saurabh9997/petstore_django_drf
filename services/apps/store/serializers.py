from rest_framework import serializers
from .models import Order


class StoreSerializer(serializers.ModelSerializer):
    # petId = serializers.IntegerField(source='pet.id')

    class Meta:
        model = Order
        fields = ['id', 'petId', 'quantity', 'shipDate', 'status', 'complete']

    def create(self, validated_data):
        pet_id = validated_data.pop('petId')
        store_instance = Order.objects.create(pet_id=pet_id, **validated_data)
        return store_instance

    def update(self, instance, validated_data):
        pet_id = validated_data.pop('petId', None)

        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.shipDate = validated_data.get('shipDate', instance.shipDate)
        instance.status = validated_data.get('status', instance.status)
        instance.complete = validated_data.get('complete', instance.complete)

        if pet_id is not None:
            instance.pet_id = pet_id

        instance.save()

        return instance
