import arrow

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from Common.models import User

# Create your models here.
def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("eqp_img_pics", hash_, filename)


class Locate(models.Model):
    def ids():
        no = Locate.objects.count()
        if no == None:
            return 1
        else:
            return no + 1

    no = models.IntegerField(_('Code'), default=ids, unique=True, editable=False)
    id = models.CharField(max_length=30, unique=True, primary_key=True, null=False, editable=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50, null=False)
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
    qr_code = models.CharField(max_length=12, unique=True, null=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(_("Equipment"), max_length=50, null=False)
    locate_id = models.ForeignKey('Locate', on_delete=models.CASCADE)
    model = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    merek = models.CharField(max_length=100, null=True)
    panjang = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    lebar = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    tinggi = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    supliyer = models.CharField(max_length=100, null=True)
    date_purchase = models.DateField(auto_now_add=False, null=True)
    eqp_img_pic = models.FileField(_('Equipment Picture'), max_length=1000, upload_to=img_url, null=True, blank=True)
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

class Spesifikasi(models.Model):
    def ids():
        no = Spesifikasi.objects.count()
        if no == None:
            return 1
        else :
            return no + 1

    no = models.IntegerField(_('Code'), default=ids, unique=True, editable=False)
    id = models.CharField(max_length = 50, unique=True, primary_key=True, null=False, editable=False)
    eqp_ids = models.ForeignKey('Equipment', on_delete=models.SET_NULL, null=True)
    s1 = models.CharField(_('Spesifikasi 1'), max_length=100, null=True)
    vs1 = models.CharField(_('Value 1'), max_length=100, null=True)
    s2 = models.CharField(_('Spesifikasi 2'), max_length=100, null=True)
    vs2 = models.CharField(_('Value 2'), max_length=100, null=True)
    s3 = models.CharField(_('Spesifikasi 3'), max_length=100, null=True)
    vs3 = models.CharField(_('Value 3'), max_length=100, null=True)
    s4 = models.CharField(_('Spesifikasi 4'), max_length=100, null=True)
    vs4 = models.CharField(_('Value 4'), max_length=100, null=True)
    s5 = models.CharField(_('Spesifikasi 5'), max_length=100, null=True)
    vs5 = models.CharField(_('Value 5'), max_length=100, null=True)
    s6 = models.CharField(_('Spesifikasi 6'), max_length=100, null=True)
    vs6 = models.CharField(_('Value 6'), max_length=100, null=True)
    s7 = models.CharField(_('Spesifikasi 7'), max_length=100, null=True)
    vs7 = models.CharField(_('Value 7'), max_length=100, null=True)
    s8 = models.CharField(_('Spesifikasi 8'), max_length=100, null=True)
    vs8 = models.CharField(_('Value 8'), max_length=100, null=True)
    s9 = models.CharField(_('Spesifikasi 9'), max_length=100, null=True)
    vs9 = models.CharField(_('Value 9'), max_length=100, null=True)
    s10 = models.CharField(_('Spesifikasi 10'), max_length=100, null=True)
    vs10 = models.CharField(_('Value 10'), max_length=100, null=True)
    s11 = models.CharField(_('Spesifikasi 11'), max_length=100, null=True)
    vs11 = models.CharField(_('Value 11'), max_length=100, null=True)
    s12 = models.CharField(_('Spesifikasi 12'), max_length=100, null=True)
    vs12 = models.CharField(_('Value 12'), max_length=100, null=True)

    def __str__(self):
        return self.id

    def save(self, **kwargs):
        if not self.id:
            self.id = "{}{:05d}".format('SPEK', self.no)
        super().save(*kwargs)
