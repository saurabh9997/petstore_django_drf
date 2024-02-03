from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from collections import Counter

from services.apps.store.models import Order
from services.apps.store.serializers import StoreSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class StoreListView(APIView):
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(request_body=StoreSerializer, responses={201: StoreSerializer()}, examples={
        "request": {"pet": 1, "quantity": 10, "shipDate": "2024-02-01T12:00:00Z", "status": "placed",
                    "complete": False},
        "response": {"id": 1, "pet": 1, "quantity": 10, "shipDate": "2024-02-01T12:00:00Z", "status": "placed",
                     "complete": False}, }, )
    def post(self, request):
        """
        Create a new store order.
        """
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StoreDetailView(APIView):
    @swagger_auto_schema(responses={200: StoreSerializer(), 204: "No Content"}, examples={
        "response": {"id": 1, "pet": 1, "quantity": 10, "shipDate": "2024-02-01T12:00:00Z", "status": "placed",
                     "complete": False}}, )
    def get(self, request, orderId):
        """
        Retrieve a specific store order.
        """
        pet = self.get_object(orderId)
        serializer = StoreSerializer(pet)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=StoreSerializer, responses={200: StoreSerializer()}, examples={
        "request": {"pet": 1, "quantity": 10, "shipDate": "2024-02-01T12:00:00Z", "status": "placed",
                    "complete": False},
        "response": {"id": 1, "pet": 1, "quantity": 10, "shipDate": "2024-02-01T12:00:00Z", "status": "placed",
                     "complete": False}, }, )
    def put(self, request, orderId):
        """
        Update a specific store order.
        """
        pet = self.get_object(orderId)
        serializer = StoreSerializer(pet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={204: "No Content"}, examples={"response": None}, )
    def delete(self, request, orderId):
        """
        Delete a specific store order.
        """
        pet = self.get_object(orderId)
        pet.delete()
        return Response(status=204)


class StoreInventory(APIView):
    # @swagger_auto_schema(responses={200: {"status": "quantity"}}, )
    def get(self, request):
        """
        Get store inventory.
        """
        orders = Order.objects.all()
        status_counter = Counter(order.status for order in orders)
        return Response(dict(status_counter))
