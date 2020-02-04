import arrow
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from Common.models import User
from Equipment.models import Equipment

# Create your models here.

class Status(models.Model):
    def ids():
        no = Status.objects.count()
        if no == None:
            return 1
        else:
            return no + 1

    no = models.IntegerField(_('Code'), default=ids, unique=True, editable=False)
    id = models.CharField(max_length=30, unique=True, primary_key=True, null=False, editable=False)
    name = models.CharField(max_length=100, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='status_created_by_user', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='status_updated_by_user', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.id = "{}{:03d}".format('ST', self.no)
        super().save(*kwargs)

class Activity(models.Model):
    def ids():
        no = Activity.objects.count()
        if no == None:
            return 1
        else:
            return no + 1

    SOURCE_CHOICES = (
            ('REQUEST','Request'),
            ('FAILURE',"Failure"),
    )

    no = models.IntegerField(_('Code'), default=ids, unique=True, editable=False)
    id = models.CharField(max_length=14, primary_key=True, unique=True, null=False, editable=False)
    equipment_ids = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='REQUEST')
    status_ids = models.ForeignKey(Status, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created_by =models.ForeignKey(User, related_name='activity_created_by_user', null=True, on_delete=models.SET_NULL)
    updated_by =models.ForeignKey(User, related_name='activity_update_by_user', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['created_on']

    def save(self, **kwargs):
        if not self.id:
            self.id = "{}{:09d}".format('ACT', self.no)
        super().save(*kwargs)
