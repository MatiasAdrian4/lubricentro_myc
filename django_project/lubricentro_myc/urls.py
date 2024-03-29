from django.urls import include, re_path
from lubricentro_myc.views.client import ClienteViewSet
from lubricentro_myc.views.db import reset
from lubricentro_myc.views.file import generar_remito_pdf, generar_stock_pdf
from lubricentro_myc.views.invoice import RemitoViewSet
from lubricentro_myc.views.invoice_item import ElementoRemitoViewSet
from lubricentro_myc.views.product import ProductoViewSet
from lubricentro_myc.views.sale import VentaViewSet
from lubricentro_myc.views.user import LoginView, LogoutView, SignupView, UserView
from rest_framework.routers import DefaultRouter

from django_project.settings import TESTING_MODE

router = DefaultRouter()
router.register(r"clientes", ClienteViewSet)
router.register(r"productos", ProductoViewSet)
router.register(r"remitos", RemitoViewSet)
router.register(r"elementos_remito", ElementoRemitoViewSet)
router.register(r"ventas", VentaViewSet)

urlpatterns = [
    re_path(r"account/signup/", SignupView.as_view()),
    re_path(r"account/login/", LoginView.as_view()),
    re_path(r"account/user/", UserView.as_view()),
    re_path(r"account/logout/", LogoutView.as_view()),
    re_path(r"generar_remito_pdf/", generar_remito_pdf, name="generar_remito_pdf"),
    re_path(r"generar_stock_pdf/", generar_stock_pdf, name="generar_stock_pdf"),
    re_path("", include(router.urls)),
]

if TESTING_MODE == 1:
    urlpatterns.append(re_path(r"reset", reset, name="reset_db"))
