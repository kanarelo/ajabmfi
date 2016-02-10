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
