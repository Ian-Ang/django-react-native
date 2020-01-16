from django.db import models
from Common.models import User
from Equipment.models import Equipment

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField(blank=True, max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='status_created_by_user', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='status_updated_by_user', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Activity(models.Model):

    SOURCE_CHOICES = (
            ('REQUEST','Request'),
            ('FAILURE',"Failure"),
    )
    id = models.CharField(max_length=14, primary_key=True, unique=True, null=False)
    equipment_ids = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='REQUEST')
    status_ids = models.ForeignKey(Status, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, default=False, null=True)
    start_time = models.TimeField(blank=True, default=False, null=True)
    end_date = models.DateField(null=True, default=False, blank=True)
    end_time = models.TimeField(null=True, default=False, blank=True)
    description = models.TextField(blank=True, max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created_by =models.ForeignKey(User, related_name='activity_created_by_user', null=True, on_delete=models.SET_NULL)
    updated_by =models.ForeignKey(User, related_name='activity_update_by_user', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['created_on']
