from django import forms
from .models import Lead

class DemoBookingForm(forms.ModelForm):
	class Meta:
		model = Lead
		exclude = [
			'modules',
			'enrollment_code'
		]