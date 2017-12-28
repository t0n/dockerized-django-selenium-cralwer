import logging

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View

from django_crawler.forms import SiteConfigurationForm
from django_crawler.models import SiteConfiguration, SiteParsingSession, SiteParsingResult
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

        logger.debug('request: ' + str(request))

        session = SiteParsingSession()
        session.save()

        site_configs = SiteConfiguration.objects.all()
        session.sites_configurations = site_configs
        session.status = 'not started'
        session.save()

        try:
            for site_config in site_configs:
                logger.debug('site_config: ' + str(site_config))
                do_crawling.delay(session.id, site_config.id)
            session.status = 'started'
            session.save()
            logger.debug('all tasks started')
        except Exception as e:
            session.status = 'failed'
            session.save()
            logger.exception(e)

        return HttpResponseRedirect(reverse('session_details', kwargs={'pk': session.id}))


class Results(ListView):
    template_name = 'results.html'
    model = SiteParsingSession


class SessionDetails(ListView):
    template_name = 'session_details.html'
    model = SiteParsingResult
    session = None

    def dispatch(self, request, *args, **kwargs):
        self.session = get_object_or_404(SiteParsingSession, id=kwargs['pk'])
        return super(SessionDetails, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return SiteParsingResult.objects.filter(session=self.session)

    def get_context_data(self, **kwargs):
        context = super(SessionDetails, self).get_context_data(**kwargs)
        context['session'] = self.session
        return context

