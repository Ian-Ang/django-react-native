import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from Common.models import Address, User
from django.contrib.auth import password_validation


class UserForm(forms.ModelForm):
    pass
    """
    password = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ["__all__"]

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
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
        return password """



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
