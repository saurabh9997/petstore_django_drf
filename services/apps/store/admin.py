from django.contrib import admin
from .models import Order
from django import forms


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'petId', 'quantity', 'shipDate', 'status', 'complete']

    def save_model(self, request, obj, form, change):
        pet_id = form.cleaned_data.get('petId', None)
        if pet_id is not None:
            obj.pet_id = pet_id
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = StoreAdminForm
        return super().get_form(request, obj, **kwargs)


class StoreAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['id', 'petId', 'quantity', 'status', 'complete']

    petId = forms.IntegerField()


admin.site.register(Order, OrderAdmin)
