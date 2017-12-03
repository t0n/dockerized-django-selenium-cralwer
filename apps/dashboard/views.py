import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
