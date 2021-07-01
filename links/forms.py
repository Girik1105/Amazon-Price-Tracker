from django import forms 
from . import models


class AddLinkForm(forms.ModelForm):

    class Meta:
        model = models.Link
        fields = ('url',)

        labels = {
            'url': '',
        }

        widgets = {
            'url': forms.TextInput(attrs={'class': '', 'id':'inputEmail', 'placeholder':'Enter the amazon link here...',}),
        }
