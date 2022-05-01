import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "lubricentro_myc.Cliente"
