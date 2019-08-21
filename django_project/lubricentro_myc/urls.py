from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from lubricentro_myc import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)
router.register(r'productos', views.ProductoViewSet)
router.register(r'remito', views.RemitoViewSet)
router.register(r'elementos_remito', views.ElementoRemitoViewSet)

urlpatterns = [
    url(r'ventas/',
        views.ventas,
        name='ventas'
    ),
    url(r'inventario/', 
        views.Inventario.as_view(),
        name='inventario'
    ),
    url(r'listado_clientes/', 
        views.ListadoClientes.as_view(),
        name='listado_clientes'
    ),
    url(r'generar_remito_pdf/',
        views.generar_remito_pdf,
        name='generar_remito_pdf'
    ),
    url(r'generar_stock_pdf/',
        views.generar_stock_pdf,
        name='generar_stock_pdf'
    ),
    url('', include(router.urls))
]