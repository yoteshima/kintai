# -*- coding: utf-8 -*-

import uuid

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserRole(models.Model):
    role_id = models.CharField(_('role id'),
                max_length=10, blank=True, null=True)
    role_name = models.CharField(_('role'),
                max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.role_name


class coustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(_('employee id'),
                primary_key=True, default=uuid.uuid4, editable=False)
    no = models.IntegerField(_('employee number'),
                blank=True, null=True, unique=True)
    username = models.CharField(_('user name'), max_length=20, default='guestuser')
    username_kana = models.CharField(_('user name kana'), max_length=20, default='guestuser')
    department = models.CharField(_('user department'), max_length=20, default='guestuser')
    roles = models.ForeignKey(UserRole,
                on_delete=models.SET_NULL, blank=True, null=True)
    joined_date = models.DateField(_('Join date'),
                blank=True, null=True)
    tel = models.CharField(_('phone number'), max_length=15,
                blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    photo = models.ImageField(upload_to='accounts/',
                blank=True, null=True)
    detail = models.TextField(_('user detail'),
                max_length=500, blank=True, null=True)
    created_date = models.DateField(_('created date'),
                blank=True, null=True, default=timezone.now)
    update_date = models.DateField(_('update date'),
                blank=True, null=True)
    status = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    
    #EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = coustomUserManager()

    @property
    def is_staff_property(self):
        return self.is_admin

    @property
    def is_superuser_property(self):
        return self.is_admin

    def __str__(self):
        return f"{self.no}_{self.username}"
