from django.urls import path

from .views import UserDetailView, UserListView

# from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'users'

urlpatterns = [path('', UserListView.as_view(), name='pet-list'),
               path('<str:username>', UserDetailView.as_view(), name='pet_details')]

# urlpatterns = format_suffix_patterns(urlpatterns)
