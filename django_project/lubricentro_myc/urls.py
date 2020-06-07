from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from lubricentro_myc import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)
router.register(r'productos', views.ProductoViewSet)
router.register(r'remito', views.RemitoViewSet)
router.register(r'elementos_remito', views.ElementoRemitoViewSet)
router.register(r'ventas_realizadas', views.VentaViewSet)

urlpatterns = [
    url(r'crear_usuario/',
        views.crear_usuario,
        name='crear_usuario'
        ),
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
    url(r'remitos/',
        views.Remitos.as_view(),
        name='remitos'
        ),
    url(r'remitos_facturacion/',
        views.remitos_facturacion,
        name='remitos_facturacion'
        ),
    url(r'ventas_historial/',
        views.HistorialVentas.as_view(),
        name='ventas_historial'
        ),
    url(r'generar_remito_pdf/',
        views.generar_remito_pdf,
        name='generar_remito_pdf'
        ),
    url(r'generar_stock_pdf/',
        views.generar_stock_pdf,
        name='generar_stock_pdf'
        ),
    url(r'acciones_csv/',
        views.CSV.as_view(),
        name='csv'
        ),
    url(r'importar_csv/',
        views.importar_csv,
        name='importar_csv'
        ),
    url(r'exportar_csv/',
        views.exportar_csv,
        name='exportar_csv'
        ),
    url('', include(router.urls))
]
