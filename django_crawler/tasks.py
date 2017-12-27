import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from django_crawler.models import SiteParsingSession, SiteConfiguration


@app.task
def do_crawling(session_id, site_configuration_id):
    session = SiteParsingSession
    configuration = SiteConfiguration()
    # UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
            'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)