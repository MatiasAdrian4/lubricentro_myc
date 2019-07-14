from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lubricentro_myc import views

router = DefaultRouter()
router.register(r'Clientes', views.ClienteViewSet)
router.register(r'Productos', views.ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]