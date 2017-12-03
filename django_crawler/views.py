import logging

from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)


class HomePage(TemplateView):
    template_name = 'index.html'
