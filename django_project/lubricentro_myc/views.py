from django.shortcuts import render
from rest_framework import viewsets

from .models import Cliente, Producto
from .serializers import ClienteSerializer, ProductoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
