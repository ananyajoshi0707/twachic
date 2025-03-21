from django import forms
from .models import SkinScan

class SkinScanForm(forms.ModelForm):
    class Meta:
        model = SkinScan
        fields = ['image']
