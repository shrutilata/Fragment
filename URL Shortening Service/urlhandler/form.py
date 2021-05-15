from django import forms
from .models import ShortUrl

class UpdateUrl(forms.ModelForm):
    class Meta:
        model=ShortUrl
        fields=["original_url","short_query","visits","user"]