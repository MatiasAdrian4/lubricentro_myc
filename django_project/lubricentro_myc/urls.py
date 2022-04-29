from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from lubricentro_myc.views.client import ClienteViewSet
from lubricentro_myc.views.file import generar_remito_pdf, importar_csv, exportar_csv, generar_stock_pdf
from lubricentro_myc.views.invoice import RemitoViewSet, ElementoRemitoViewSet
from lubricentro_myc.views.product import ProductoViewSet
from lubricentro_myc.views.sale import VentaViewSet
from lubricentro_myc.views.user import crear_usuario
from lubricentro_myc.views import template

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'remito', RemitoViewSet)
router.register(r'elementos_remito', ElementoRemitoViewSet)
router.register(r'ventas_realizadas', VentaViewSet)

urlpatterns = [
    re_path(r'crear_usuario/',
        crear_usuario,
        name='crear_usuario'
        ),
    re_path(r'ventas/',
        template.ventas,
        name='ventas'
        ),
    re_path(r'inventario/',
        template.Inventario.as_view(),
        name='inventario'
        ),
    re_path(r'listado_clientes/',
        template.ListadoClientes.as_view(),
        name='listado_clientes'
        ),
    re_path(r'remitos/',
        template.Remitos.as_view(),
        name='remitos'
        ),
    re_path(r'remitos_facturacion/',
        template.remitos_facturacion,
        name='remitos_facturacion'
        ),
    re_path(r'remitos_edicion/',
        template.RemitosEdicion.as_view(),
        name='remitos_edicion'
        ),
    re_path(r'ventas_historial/',
        template.HistorialVentas.as_view(),
        name='ventas_historial'
        ),
    re_path(r'generar_remito_pdf/',
        generar_remito_pdf,
        name='generar_remito_pdf'
        ),
    re_path(r'acciones_csv/',
        template.CSV.as_view(),
        name='csv'
        ),
    re_path(r'importar_csv/',
        importar_csv,
        name='importar_csv'
        ),
    re_path(r'exportar_csv/',
        exportar_csv,
        name='exportar_csv'
        ),
    re_path(r'impresion_stock/',
        template.ImpresionStock.as_view(),
        name="impresion_stock"
        ),
    re_path(r'generar_stock_pdf/',
        generar_stock_pdf,
        name='generar_stock_pdf'
        ),
    re_path('', include(router.urls))
]
