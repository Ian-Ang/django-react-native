from django.db import models
from Common.models import User
from Equipment.models import Equipment

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField(blank=True, max_length=255, null=True)

    def __str__(self):
        return self.name

class Activity(models.Model):

    SOURCE_CHOICES = (
            ('REQUEST','Request'),
            ('FAILURE',"Failure"),
    )
    id = models.CharField(max_length=14, primary_key=True, unique=True, null=False)
    created = models.DateTimeField(auto_now_add=True)
    equipment_ids = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='REQUEST')
    status_ids = models.ForeignKey(Status, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, default=False, null=True)
    end_date = models.DateTimeField(null=True, default=False, blank=True)
    Created_by =models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, max_length=255, null=True)

    class Meta:
        ordering = ['created']
