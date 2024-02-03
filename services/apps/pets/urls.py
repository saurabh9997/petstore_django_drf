from django.urls import path

from .views import PetDetailsByStatusView, PetDetailView, PetListView

app_name = 'pets'

urlpatterns = [path('', PetListView.as_view(), name='pet'),
               path('/findByStatus', PetDetailsByStatusView.as_view(), name='pet-details-by-status'),
               path('/<int:petId>', PetDetailView.as_view(), name='pet_details')]
