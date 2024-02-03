from django.http import Http404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import CustomUser
from .serializers import UserSerializer


class UserTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data['refresh']
            access_token = response.data['access']

            # Attach the refresh token to the response data
            response.data[
                'refresh_token'] = refresh_token  # Store the refresh token in the user's session or any other secure
            # place

        return response


class UserTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data['refresh']

            # Attach the refresh token to the response data
            response.data[
                'refresh_token'] = refresh_token  # Store the refresh token in the user's session or any other secure
            # place

        return response


class UserTokenLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            # Blacklist the refresh token to invalidate it
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Logout successful."}, status=200)
            except Exception as e:
                return Response({"detail": "Invalid token."}, status=400)
        else:
            return Response({"detail": "Refresh token not provided."}, status=400)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserListView(APIView):
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.all()

        # pagination logic
        page_size = self.pagination_class.page_size
        page = int(request.GET.get('page', 1))
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_queryset = CustomUser[start_index:end_index]

        serializer = UserSerializer(paginated_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get_object(self, username):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, username):
        pet = self.get_object(username)
        serializer = UserSerializer(pet)
        return Response(serializer.data)

    def put(self, request, username):
        pet = self.get_object(username)
        serializer = UserSerializer(pet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        pet = self.get_object(username)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
