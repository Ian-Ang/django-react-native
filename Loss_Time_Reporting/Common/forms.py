import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from Common.models import Address, User
from django.contrib.auth import password_validation


class UserForm(forms.ModelForm):
    
    password = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'role', 'profile_pic', 'has_manager_access',
                  'has_supervisor_access', 'has_staff_access']

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        if not self.instance.pk:
            self.fields['password'].required = True

        # self.fields['password'].required = True

    # def __init__(self, args: object, kwargs: object) -> object:
    #     super(UserForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['first_name'].required = True
    #     self.fields['username'].required = True
    #     self.fields['email'].required = True
    #
        # if not self.instance.pk:
        #     self.fields['password'].required = True

    def clean_password(self):
        password = self.clean_password.get('password')
        if password:
            if len(password)<4:
                raise form.ValidationError('Password must be at last 4 characters long!')
        return password

    def clean_has_manager_access(self):
        manager = self.cleaned_data.get('has_manager_access', False)
        if user_role == 'ADMIN':
            is_admin = True
        else:
            is_admin = False
        if self.request_user.role == 'ADMIN' or self.request_user.is_superuser:
            if not is_admin:
                superpisor = self.data.get('has_supervisor_access', False)
                staff = self.data.get('has_staff_access', False)
                if not manager and not superpisor and not staff:
                    raise form.ValidationError('Selest atleast one option.')
        if self.request_user.role == 'USER':
            manager = self.instance.has_manager_access
        return manager

    def clean_has_supervisor_access(self):
        superpisor = self.cleaned_data.get('has_supervisor_access', False)
        if user_role == 'ADMIN':
            is_admin = True
        else:
            is_admin = False
        if self.request_user.role == 'ADMIN' or self.request_user.is_superuser:
            if not is_admin:
                manager = self.data.get('has_manager_access', False)
                staff = self.data.get('has_staff_access', False)
                if not manager and not superpisor and not staff:
                    raise form.ValidationError('Selest atleast one option.')
        if self.request_user.role == 'USER':
            manager = self.instance.has_supervisor_access
        return superpisor

    def clean_has_staff_access(self):
        staff = self.cleaned_data.get('has_staff_access', False)
        if self.request_user.role == 'USER':
            staf = self.instance.has_staff_access
        return staff

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if self.instance.id:
            if self.instance.email != email:
                if not User.objects.filter(email=self.cleaned_data.get("email")).exists():
                    return self.cleaned_data.get("email")
                raise form.ValidationError('Email already exists')
            else:
                return self.cleaned_data.get("email")
        else:
            if not User.objects.filter(email=self.cleaned_data.get("email")).exists():
                return self.cleaned_data.get("email")
            raise form.ValidationError('User already exists with this email')


class LoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 4:
                raise forms.ValidationError(
                    'Password must be at least 4 characters long!')
        return password

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user:
                if not self.user.is_active:
                    pass
                    # raise forms.ValidationError("User is Inactive")
            else:
                pass
                # raise forms.ValidationError("Invalid email and password")
        return self.cleaned_data

class ChangePasswordForm(forms.Form):
    # CurrentPassword = forms.CharField(max_length=100)
    Newpassword = forms.CharField(max_length=100)
    confirm = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_confirm(self):
        # if len(self.data.get('confirm')) < 4:
        #     raise forms.ValidationError(
        #         'Password must be at least 4 characters long!')
        if self.data.get('confirm') != self.cleaned_data.get('Newpassword'):
            raise forms.ValidationError('Confirm password do not match with new password')
        password_validation.validate_password(self.cleaned_data.get('Newpassword'), user=self.user)
        return self.data.get('confirm')

class PasswordResetEmailForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email_iexact=email, is_active=True).exists():
            raise form.ValidationError("User doesn't exist with Email")
        return email
