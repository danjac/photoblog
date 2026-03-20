import factory
from factory.django import DjangoModelFactory

from photoblog.photos.models import Photo
from photoblog.users.tests.factories import UserFactory


class PhotoFactory(DjangoModelFactory):
    class Meta:
        model = Photo

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("word")
    description = factory.Faker("paragraph")
