from django import forms

from django_crawler.models import SiteConfiguration


class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        exclude = ()
