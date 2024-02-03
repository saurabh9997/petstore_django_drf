# pets/admin.py
from django.contrib import admin

from .models import Category, Pet, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'status', 'created_at', 'updated_at')
    list_filter = ('category', 'status')
    search_fields = ('name', 'category__name', 'status')
    readonly_fields = ('created_at', 'updated_at')
