from django import forms
from Common.models import User
from django.db.models import Q
from Equipment.models import Equipment
from Activity.models import Activity, Status

class ActivityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop('request_user', None)
        self.obj_instance = kwargs.get('instance', None)
        super(ActivityForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        if request_user.role == 'ADMIN' or request_user.is_superuser:
            self.fields["equipment_ids"].queryset = Equipment.objects.filter(is_active=True)
            self.fields["status_ids"].queryset = Status.objects.filter(is_active=True)

        if request_user.role == 'USER':
            self.fields["equipment_ids"].queryset = Equipment.objects.filter(Q(created_by=request_user) | Q(is_active=True))
            self.fields["status_ids"].queryset = Status.objects.filter(Q(create_by=request_user)) | Q(is_active=True)

        self.fields['source'].required = True
        self.fields['start_date'].required = True
        self.fields['start_time'].required = True
        self.fields['end_date'].required = False
        self.fields['end_time'].required = False
        self.fields['is_active'].required = True
        self.fields['description'].required = False

    def clean_status(self):
        status = self.cleaned_data.get('status_ids')
        if not self.obj_instance:
            if Activity.objects.filter(Q(status_ids=status_ids) & Q(is_active =True)).exists():
                raise forms.ValidationError('Activity with this status already exists')
            return status
        if Activity.objects.filter(Q(status_ids=status_ids) & Q(is_active =True)).exclude(id=self.obj_instance.id).exists():
            raise forms.ValidationError('Activity with this status already exists')
            return status
        return status

    class Meta:
        model = Activity
        fields = ('equipment_ids','source','status_ids','start_date','start_time','end_date','end_time','is_active','description')


class StatusForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop('request_user', None)
        self.obj_instance = kwargs.get('instance', None)
        super(StatusForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        self.fields['name'].required = True
        self.fields['is_active'].required = True
        self.fields['description'].required = False

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not self.obj_instance:
            if Status.objects.filter(name=name).exists():
                raise form.ValidationError('Status with name already exists')
            return name
        if Status.objects.filter(name=name).exclude(id=self.obj_instance.id).exists():
            raise form.ValidationError('Status with name already exists')
            return name
        return name

    class Meta:
        model = Status
        fields = ('name','is_active','description')
