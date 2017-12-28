import logging

from celery.task import task
from celery.utils.log import get_task_logger

from django_crawler.crawler import Crawler
from django_crawler.models import SiteParsingSession, SiteConfiguration

logger = get_task_logger(__name__)


@task(name="do_crawling")
def do_crawling(session_id, site_configuration_id):
    logger('do_crawling: {0}, {1}'.format(session_id, site_configuration_id))
    session = SiteParsingSession.objects.get(id=session_id)
    configuration = SiteConfiguration.objects.get(id=site_configuration_id)
    crawler = Crawler()
    return crawler.do_crawling('http://google.com')