from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from services.apps.pets.models import Pet
from services.apps.pets.serializers import PetSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PetListView(APIView):
    pagination_class = StandardResultsSetPagination

    # def get(self, request):
    #     """
    #     Retrieve a paginated list of pets.
    #     """
    #     pets = Pet.objects.all()
    #
    #     # Pagination logic
    #     page_size = self.pagination_class.page_size
    #     page = int(request.GET.get('page', 1))
    #     start_index = (page - 1) * page_size
    #     end_index = start_index + page_size
    #     paginated_queryset = pets[start_index:end_index]
    #
    #     serializer = PetSerializer(paginated_queryset, many=True)
    #     return Response(serializer.data)

    @swagger_auto_schema(request_body=PetSerializer, responses={201: PetSerializer()}, examples={
        "request": {"name": "New Pet", "category": {"id": 1, "name": "Example Category"},
                    "tags": [{"id": 1, "name": "Example Tag"}], "status": "available", },
        "response": {"id": 1, "name": "New Pet", "category": {"id": 1, "name": "Example Category"},
                     "tags": [{"id": 1, "name": "Example Tag"}], "status": "available", }, }, )
    def post(self, request):
        """
        Create a new pet.
        """
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PetSerializer, responses={201: PetSerializer()}, examples={
        "request": {"name": "New Pet", "category": {"id": 1, "name": "Example Category"},
                    "tags": [{"id": 1, "name": "Example Tag"}], "status": "available", },
        "response": {"id": 1, "name": "Updated Pet", "category": {"id": 1, "name": "Updated Category"},
                     "tags": [{"id": 1, "name": "Updated Tag"}], "status": "updated", }, }, )
    def put(self, request):
        """
        Update an existing pet.
        """
        pet_id = request.data.get('id', None)
        if pet_id:
            pet = get_object_or_404(Pet, id=pet_id)
            serializer = PetSerializer(pet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Please provide the 'id' of the pet to be updated."},
                status=status.HTTP_400_BAD_REQUEST)


class PetDetailView(APIView):
    @swagger_auto_schema(responses={200: PetSerializer()}, examples={
        "response": {"id": 1, "name": "Example Pet", "category": {"id": 1, "name": "Example Category"},
                     "tags": [{"id": 1, "name": "Example Tag"}], "status": "available", }, }, )
    def get_object(self, petId):
        try:
            return Pet.objects.get(pk=petId)
        except Pet.DoesNotExist:
            raise Http404

    def get(self, request, petId):
        """
        Retrieve details of a specific pet.
        """
        pet = self.get_object(petId)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PetSerializer, responses={200: PetSerializer()}, examples={
        "request": {"name": "Updated Pet", "category": {"id": 1, "name": "Example Category"},
                    "tags": [{"id": 1, "name": "Example Tag"}], "status": "available", },
        "response": {"id": 1, "name": "Updated Pet", "category": {"id": 1, "name": "Example Category"},
                     "tags": [{"id": 1, "name": "Example Tag"}], "status": "available", }, }, )
    def put(self, request, petId):
        """
        Update details of a specific pet.
        """
        pet = self.get_object(petId)
        serializer = PetSerializer(pet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No Content"}, examples={"response": None}, )
    def delete(self, request, petId):
        """
        Delete a specific pet.
        """
        pet = self.get_object(petId)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PetDetailsByStatusView(APIView):
    @swagger_auto_schema(responses={200: PetSerializer(many=True)}, examples={"response": [
        {"id": 1, "name": "Example Pet", "category": {"id": 1, "name": "Example Category"},
         "tags": [{"id": 1, "name": "Example Tag"}], "status": "available", },  # Add more examples as needed
    ]}, )
    def get(self, request):
        """
        Retrieve a list of pets by status.
        """
        status_values = request.GET.get('status')
        if status_values:
            status_list = status_values.split(',')
            pets = Pet.objects.filter(status__in=status_list)
            serializer = PetSerializer(pets, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Please provide at least one status value."}, status=status.HTTP_400_BAD_REQUEST)
