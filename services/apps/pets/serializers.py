from rest_framework import serializers

from .models import Category, Pet, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class PetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Pet
        fields = ['id', 'name', 'category', 'tags', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        tags_data = validated_data.pop('tags')

        category_instance, _ = Category.objects.get_or_create(**category_data)
        tags_instances = [Tag.objects.get_or_create(**tag_data)[0] for tag_data in tags_data]

        pet_instance = Pet.objects.create(category=category_instance, **validated_data)
        pet_instance.tags.set(tags_instances)

        return pet_instance

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', {})
        tags_data = validated_data.pop('tags', [])

        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)

        instance.category, _ = Category.objects.get_or_create(**category_data)

        tags_instances = [Tag.objects.get_or_create(**tag_data)[0] for tag_data in tags_data]
        instance.tags.set(tags_instances)

        instance.save()

        return instance
