import factory
from apps.users.factories import UserFactory
from django.conf import settings

from sparkplug_avatars.models.avatar import Avatar


class AvatarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Avatar

    creator = factory.SubFactory(UserFactory)
    file = factory.django.ImageField(filename="avatar.jpg")
