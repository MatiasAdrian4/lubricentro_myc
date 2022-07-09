import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "lubricentro_myc.Cliente"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "lubricentro_myc.Producto"


class SaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "lubricentro_myc.Venta"

    producto_id = 1
    cantidad = 1.0
    precio = 1.0


class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "lubricentro_myc.Remito"


class InvoiceItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "lubricentro_myc.ElementoRemito"
