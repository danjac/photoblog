import factory
from factory.django import DjangoModelFactory, ImageField

from photoblog.photos.models import Photo, Tag
from photoblog.users.tests.factories import UserFactory


class PhotoFactory(DjangoModelFactory):
    class Meta:
        model = Photo

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    image = ImageField(color="blue")


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    tag = factory.Faker("word")
