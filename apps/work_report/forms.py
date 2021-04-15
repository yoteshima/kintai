from django import forms

from .models import WorkDetail

class TimeStampForm(forms.ModelForm):

    class Meta:
        model = WorkDetail
        fields = ('start_time', 'end_time',)