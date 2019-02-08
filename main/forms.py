from django import forms
from .models import EmissionInYear

class GetEmissionsForm(forms.Form):

    country = forms.CharField(max_length=50)

    percapita = forms.BooleanField()
