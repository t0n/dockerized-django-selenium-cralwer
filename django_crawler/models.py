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
