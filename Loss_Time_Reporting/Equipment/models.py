import arrow

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from Common.models import User

# Create your models here.
class Locate(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True, null=False)
    name = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, max_length=255)
    created_on = models.DateTimeField(_('Created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('Updated on'), auto_now_add=False, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='locate_created_by_user', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='locate_updated_by_user', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    id = models.CharField(max_length=7, unique=True, primary_key=True, null=False)
    locate_id = models.ForeignKey('Locate', on_delete=models.CASCADE)
    name = models.CharField(_("Equipment"), max_length=50, null=False)
    qr_code = models.CharField(max_length=12, unique=True, null=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, max_length=255)
    created_on = models.DateTimeField(_('Created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('Updated on'), auto_now_add=False, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='equipment_created_by_user', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='equipment_updated_by_user', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()
