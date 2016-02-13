from django import forms
from . import api as auth_api

class BaseUserAddForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    middle_name = forms.CharField(max_length=50, required=True)
    surname = forms.CharField(max_length=50, required=True)

    email = forms.EmailField(max_length=255, required=True)

    role = forms.IntegerField(required=True)

    def clean_role(self):
        role = self.cleaned_data.get('role')
        
        if not auth_api.role_exists(id=role):
            raise forms.ValueError('Role not found')

        return role

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        middle_name = self.cleaned_data.get('middle_name')
        surname = self.cleaned_data.get('surname')

        full_name = "%s %s %s" % (first_name, middle_name, surname)
 
        if not full_name.strip():
            raise forms.ValueError("Please provide a valid Name")

        return self.cleaned_data

class AddPartnerUserForm(BaseUserAddForm):
    pass

class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_repeat = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_repeat = self.cleaned_data.get('new_password_repeat')

        if new_password_repeat != new_password:
            raise form.ValidationError('The two passwords do not match!')

        return self.cleaned_data

class ChangeUserPasswordForm(ChangePasswordForm):
    current_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, data=None, user=None, *args, **kwargs):
        self.user = user

        super(ChangeUserPasswordForm, self).__init__(data=data, *args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')

        if not self.user.check_password(current_password):
            raise forms.ValidationError('Authorization denied, wrong current password entered')

        return current_password
