from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from extra.mixins import UUIDIdMixin

class AccountManager(BaseUserManager):
    def create_user(self, **kwargs):
        if not kwargs.get('email'):
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('password'):
            raise ValueError('Users must have a valid password.')

        account = self.model(
            email=self.normalize_email(kwargs.get('email', None)),
        )

        account.set_password(kwargs.get('password'))
        account.save()

        return account

    def create_superuser(self, **kwargs):
        account = self.create_user(**kwargs)

        account.is_admin = True
        account.save()

        return account

class Account(AbstractBaseUser, PermissionsMixin, UUIDIdMixin):
    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email
