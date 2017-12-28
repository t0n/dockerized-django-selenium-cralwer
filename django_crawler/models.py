from django.db import models
from django.utils.translation import ugettext_lazy as _


class SiteConfiguration(models.Model):
    url = models.CharField(_('Site URL'), max_length=4000)
    enabled = models.BooleanField(_('Site Enabled'), default=True)

    class Meta:
        verbose_name = _('Site Configuration')
        verbose_name_plural = _('Site Configurations')

    def __str__(self):
        return '{} [{}]'.format(self.url, self.enabled)


class SiteParsingSession(models.Model):
    sites_configurations = models.ManyToManyField(SiteConfiguration)
    status = models.CharField(max_length=100)

    def get_total_sites(self):
        return self.sites_configurations.count()

    def get_results_count(self):
        return self.session_results.all().count()


class SiteParsingResult(models.Model):
    site = models.ForeignKey(SiteConfiguration)
    session = models.ForeignKey(SiteParsingSession, related_name='session_results')
    html = models.TextField(default='')
