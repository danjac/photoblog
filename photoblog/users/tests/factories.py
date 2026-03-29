from allauth.account.models import EmailAddress
from factory import django
from factory.declarations import LazyAttribute, SubFactory
from factory.faker import Faker

from photoblog.users.models import User


class UserFactory(django.DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    password = django.Password("testpass")

    class Meta:
        model = User


class EmailAddressFactory(django.DjangoModelFactory):
    user = SubFactory(UserFactory)
    email = LazyAttribute(lambda a: a.user.email)
    verified = True

    class Meta:
        model = EmailAddress
