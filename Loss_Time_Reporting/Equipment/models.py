from django.db import models

# Create your models here.
class Locate(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True, null=False)
    name = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, max_length=255)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    id = models.CharField(max_length=7, unique=True, primary_key=True, null=False)
    locate_id = models.ForeignKey('Locate', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, max_length=255)
    qr_code = models.CharField(max_length=12, unique=True, null=False)

    def __str__(self):
        return self.name
