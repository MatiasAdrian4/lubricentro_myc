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

    cantidad = 1
    producto_id = 1
