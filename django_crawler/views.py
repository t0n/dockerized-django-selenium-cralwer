import logging

from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from django_crawler.forms import SiteConfigurationForm
from django_crawler.models import SiteConfiguration

logger = logging.getLogger(__name__)


class HomePage(ListView):
    template_name = 'index.html'
    model = SiteConfiguration


class SiteConfigurationCreateView(CreateView):
    template_name = 'site_configuration_form.html'
    model = SiteConfiguration
    form_class = SiteConfigurationForm
    success_url = reverse_lazy('home')
