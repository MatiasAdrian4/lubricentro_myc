from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from lubricentro_myc.views import ClienteViewSet, ProductoViewSet, ProductoListView

router = DefaultRouter()
#router.register(r'Clientes', ClienteViewSet)
#router.register(r'Productos', ProductoViewSet)

urlpatterns = [
    url(r'productos/', 
        ProductoListView.as_view(),
        name='productos'
    ),
    url('', include(router.urls))
]