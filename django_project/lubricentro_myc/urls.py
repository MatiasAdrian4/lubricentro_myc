from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from lubricentro_myc.views import ClienteViewSet, ProductoViewSet, InventarioView

router = DefaultRouter()
#router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    url(r'inventario/', 
        InventarioView.as_view(),
        name='inventario'
    ),
    url('', include(router.urls))
]