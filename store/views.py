from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response


from . import models
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductsSerializer


class ProductListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'rating']


class Product(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = "slug"
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryItemView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProductSerializer

    # this function is used to retrive all products with the desired category or its decendents
    def get_queryset(self):
        return models.Product.objects.filter(
            category__in=Category.objects.get(
                slug=self.kwargs["slug"]).get_descendants(include_self=True)
        )


class CategoryListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Category.objects.filter(
        level=0).get_descendants(include_self=True)
    serializer_class = CategorySerializer
