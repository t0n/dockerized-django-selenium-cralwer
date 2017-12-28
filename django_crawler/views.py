import logging

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View

from django_crawler.forms import SiteConfigurationForm
from django_crawler.models import SiteConfiguration, SiteParsingSession
from django_crawler.tasks import do_crawling

logger = logging.getLogger(__name__)


class HomePage(ListView):
    template_name = 'index.html'
    model = SiteConfiguration


class SiteConfigurationCreateView(CreateView):
    template_name = 'site_configuration_form.html'
    model = SiteConfiguration
    form_class = SiteConfigurationForm
    success_url = reverse_lazy('home')


class StartCrawling(View):

    def get(self, request):

        print('request: ' + str(request))

        session = SiteParsingSession()
        session.save()

        site_configs = SiteConfiguration.objects.all()
        session.sites_configurations = site_configs
        session.save()

        for site_config in site_configs:
            print('site_config: ' + str(site_config))
            do_crawling.delay(session.id, site_config.id)

        return HttpResponseRedirect(reverse('home'))
