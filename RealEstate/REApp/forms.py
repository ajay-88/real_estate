from django import forms
from REApp.models import Feedback
class Feedback_form(forms.ModelForm):
    class Meta:
        model=Feedback
        fields = ["Name","Gmail","Message"]