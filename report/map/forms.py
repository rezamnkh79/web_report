from django import forms
from .models import Poit_Info
import datetime


class PointForm(forms.ModelForm):
    # time = forms.TimeField()
    class Meta:
        # specify model to be used
        model = Poit_Info
        
        # specify fields to be used
        fields = [
            "Accuracy",
            "latitude",
            "longitude",
            "Code",
            "Power"]
            