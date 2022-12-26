from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from store.models import Product
from store.serializers import ProductSerializer, AdminProductSerializer
from bidding import models
from bidding.serializers import AdminBidSerializer
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.


class UpdateDeleteProductView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Product.objects.all()
    lookup_field = "slug"
    serializer_class = ProductSerializer


class CreateProductView(generics.CreateAPIView):
    # permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Product.objects.all()
    serializer_class = AdminProductSerializer


class GetProductBids(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = AdminBidSerializer

    def get_queryset(self):
        product_instance = get_object_or_404(Product, slug=self.kwargs["slug"])
        return models.Bid.objects.filter(product=product_instance).order_by("-bidding_amount")
