import datetime
import os
import time
from django.db import models
from django.utils import timezone
from Common.utils import COUNTRIES, ROLES
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)

# Create your models here.

def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)

class User(AbstractBaseUser, PermissionsMixin):
    file_prepend = "user/profile_pics"
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_('username'), max_length=100, unique=True,
                                help_text=_('Required. 8 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator],
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                },)
    first_name = models.CharField(_('First Name'), max_length=150, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=150, blank=True)
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_admin = models.BooleanField(_('Is Admin'), default=False)
    is_staff = models.BooleanField(_('Is Staff'), default=False)
    date_joined = models.DateTimeField(('Date Joined'), auto_now_add=True)
    role = models.CharField(_('Role'), max_length=50, choices=ROLES)
    profile_pic = models.FileField(_('Profile Picture'), max_length=1000, upload_to=img_url, null=True, blank=True)
    has_manager_access = models.BooleanField(_('Manager Access'),default=False)
    has_supervisor_access = models.BooleanField(_('Supervisor Access'),default=False)
    has_staff_access = models.BooleanField(_('Staff Access'),default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def gef_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        elif self.username :
            full_name = self.username
        else:
            full_name = self.email
        return full_name

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-is_active']

class Address(models.Model):
    address_line = models.CharField(_("Address"), max_length=255, blank=True, null=False)
    street = models.CharField(_("Street"), blank=True, max_length=55, null=True)
    city = models.CharField(_("City"), blank=True, max_length=255, null=True)
    state = models.CharField(_("State"), blank=True, max_length=255, null=True)
    postcode = models.CharField(_("Post/Zip-code"), blank=True, max_length=64, null=True)
    country = models.CharField(_("Country"), blank=True, max_length=3, null=True, choices=COUNTRIES)

    def __str__(self):
        return self.city if self.city else ""

    def get_complete_address(self):
        address = ""
        if self.address_line:
            address += self.address_line
        if self.street:
            if address:
                address += ", " + self.street
            else:
                address += self.street
        if self.city:
            if address:
                address += ", " + self.city
            else:
                address += self.city
        if self.state:
            if address:
                address += ", " + self.state
            else:
                address += self.state
        if self.postcode:
            if address:
                address += ", " + self.postcode
            else:
                address += self.postcode
        if self.country:
            if address:
                address += ", " + self.get_country_display()
            else:
                address += self.get_country_display()
        return address
