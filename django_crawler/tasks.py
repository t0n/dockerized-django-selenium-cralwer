import logging

from celery.task import task
from celery.utils.log import get_task_logger
from django.core.exceptions import ObjectDoesNotExist

from django_crawler.crawler import Crawler
from django_crawler.models import SiteParsingSession, SiteConfiguration, SiteParsingResult

logger = get_task_logger(__name__)


@task(name="do_crawling")
def do_crawling(session_id, site_configuration_id):
    logger.debug('do_crawling: {0}, {1}'.format(session_id, site_configuration_id))

    session = SiteParsingSession.objects.get(id=session_id)
    configuration = SiteConfiguration.objects.get(id=site_configuration_id)
    logging.debug('do_crawling: session: ' + str(session))
    logging.debug('do_crawling: configuration: ' + str(configuration))

    parsing_result = SiteParsingResult(site=configuration, session=session)
    parsing_result.save()

    logger.debug('do_crawling starting crawling for url: ' + configuration.url)
    try:
        crawler = Crawler()
        html = crawler.do_crawling(configuration.url)

        parsing_result.html = html
        parsing_result.save()

        done = True
        all_configs = session.sites_configurations.all()
        for config in all_configs:
            try:
                result = SiteParsingResult.objects.get(session=session, site=config)
                if not result or not result.html:
                    done = False
            except ObjectDoesNotExist:
                done = False
        if done:
            session.status = 'done'
            session.save()

        logger.debug('do_crawling crawling done!')
    except Exception as e:
        logger.debug('error: ' + str(e))

    return parsing_result.id
