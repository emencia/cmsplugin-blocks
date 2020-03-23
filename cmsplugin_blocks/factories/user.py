# -*- coding: utf-8 -*-
import factory

from django.conf import settings
from django.contrib.auth.hashers import make_password


class UserFactory(factory.django.DjangoModelFactory):
    """
    Create a fake user with Faker.
    """

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = make_password("password")
