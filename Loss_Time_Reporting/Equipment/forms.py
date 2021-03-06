from django import forms
from uuid import uuid4
from Common.models import User
from django.db.models import Q
from Equipment.models import Equipment, Locate
from Teams.models import Teams

class EquipmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop('request_user', None)
        self.obj_instance = kwargs.get('instance', None)
        super(EquipmentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        if request_user.role == 'ADMIN' or request_user.is_superuser:
            self.fields["locate_id"].queryset = Locate.objects.filter(is_active=True)

        if request_user.role == 'USER':
            self.fields["locate_id"].queryset = Locate.objects.filter(Q(created_by=request_user) | Q(is_active=True))

        self.fields['name'].required = True
        self.fields['locate_id'].required = True
        self.fields['model'].required = False
        self.fields['type'].required = False
        self.fields['merek'].required = True
        self.fields['panjang'].required = False
        self.fields['lebar'].required = False
        self.fields['tinggi'].required = False
        self.fields['supliyer'].required = False
        self.fields['date_purchase'].required = False
        self.fields['eqp_img_pic'].required = False
        self.fields['qr_code'].required = False
        self.fields['is_active'].required = False
        self.fields['description'].required = False

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not self.obj_instance:
            if Equipment.objects.filter(name=name).exists():
                raise forms.ValidationError('Equipment with this name already exists')
            return name
        if Equipment.objects.filter(name=name).exclude(id=self.obj_instance.id).exists():
            raise forms.ValidationError('Equipment with this name already exists')
            return name
        return name

    class Meta:
        model = Equipment
        fields = ('locate_id','name','qr_code','is_active','description','model','type','panjang','lebar','tinggi','merek','date_purchase','eqp_img_pic','supliyer')


class LocateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop('request_user', None)
        self.obj_instance = kwargs.get('instance', None)
        super(LocateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class":"form-control"}

        self.fields['name'].required = True
        self.fields['parent'].required = False
        self.fields['is_active'].required = False
        self.fields['description'].required = False

    class Meta:
        model = Locate
        fields = ('name', 'parent', 'is_active', 'description')
