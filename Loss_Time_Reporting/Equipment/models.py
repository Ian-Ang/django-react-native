import arrow

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from Common.models import User

# Create your models here.
class Locate(models.Model):
    def ids():
        no = Equipment.objects.count()
        if no == None:
            return 1
        else:
            return no + 1

    no = models.IntegerField(_('Code'), default=ids, unique=True, editable=False)
    id = models.CharField(max_length=30, unique=True, primary_key=True, null=False, editable=False)
    name = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, max_length=255)
    created_on = models.DateTimeField(_('Created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('Updated on'), auto_now_add=False, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='locate_created_by_user', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='locate_updated_by_user', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.id = "{}{:05d}".format('LCT', self.no)
        super().save(*kwargs)


class Equipment(models.Model):

    def ids():
        no = Equipment.objects.count()
        if no == None:
            return 1
        else:
            return no + 1

    no = models.IntegerField(_('Code'), default=ids, unique=True, editable=False)
    id = models.CharField(max_length=30, unique=True, primary_key=True, null=False, editable=False)
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

    def save(self, **kwargs):
        if not self.id:
            self.id = "{}{:08d}".format('EQP', self.no)
        super().save(*kwargs)
