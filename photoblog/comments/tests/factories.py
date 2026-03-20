import factory
from factory.django import DjangoModelFactory

from photoblog.comments.models import Comment
from photoblog.photos.tests.factories import PhotoFactory
from photoblog.users.tests.factories import UserFactory


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    photo = factory.SubFactory(PhotoFactory)
    comment = factory.Faker("paragraph")
