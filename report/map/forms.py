from django import forms
from .models import Point_Info
import datetime


class PointForm(forms.ModelForm):
    # time = forms.TimeField()
    class Meta:
        # specify model to be used
        model = Point_Info
        
        # specify fields to be used
        fields = [
            
            "latitude",
            "longitude",
            "code",
            "power"]
            