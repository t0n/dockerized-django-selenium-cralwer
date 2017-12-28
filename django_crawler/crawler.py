from selenium import webdriver
import logging
import time

from selenium.webdriver import DesiredCapabilities, FirefoxProfile

logger = logging.getLogger(__name__)


class Crawler(object):

    def __init__(self):
        super(Crawler, self).__init__()
        selenium_configuration = {
            'SELENIUM_HOST': 'selenium',
            'SELENIUM_PORT': '4444',
        }
        self.driver = self._get_driver(selenium_configuration)

    def _get_driver(self, selenium_configuration):
        logger.debug('_get_driver started')
        driver = self._create_firefox_driver(selenium_configuration)
        # driver.maximize_window()
        return driver

    def _create_firefox_driver(self, selenium_configuration):
        logger.debug('_create_firefox_driver got selenium configuration, creating special driver...')

        selenium_host = selenium_configuration['SELENIUM_HOST']
        selenium_port = selenium_configuration['SELENIUM_PORT']
        logger.debug('_create_firefox_driver selenium_host: ' + str(selenium_host))
        logger.debug('_create_firefox_driver selenium_port: ' + str(selenium_port))

        executor_url = 'http://{0}:{1}/wd/hub'.format(selenium_host, selenium_port)
        logger.debug('_create_firefox_driver executor_url: ' + executor_url)

        dcaps = DesiredCapabilities.FIREFOX
        dcaps['javascriptEnabled'] = True
        logger.debug('_create_firefox_driver DesiredCapabilities: ' + str(dcaps))

        firefox_profile = FirefoxProfile()
        logger.debug('_create_firefox_driver firefox_profile: ' + str(firefox_profile))

        driver = self._create_remote_firefox_driver_with_retries(executor_url, dcaps, firefox_profile)
        return driver

    def _create_remote_firefox_driver_with_retries(self, executor_url, dcaps, firefox_profile):
        retry = True
        retries_max_count = 3
        retries = 0
        driver = None
        while retry:
            try:
                driver = webdriver.Remote(
                    command_executor=executor_url,
                    desired_capabilities=dcaps,
                    browser_profile=firefox_profile
                )
                retry = False if driver else True
            except Exception:
                logger.exception('Cannot create driver')
                logger.debug('_get_driver Cannot create driver, retrying')
            if retry:
                retries += 1
                logger.debug('_get_driver retrying, retries count: {}'.format(retries))
                if retries <= retries_max_count:
                    seconds_to_sleep = 5 + (retries * 10)
                    logger.debug('_get_driver retrying, sleeping for {} seconds'.format(seconds_to_sleep))
                    time.sleep(seconds_to_sleep)
                else:
                    logger.debug('_get_driver retries limit exceeded')
                    retry = False

        if driver is None:
            logger.error('Cannot create driver')
        return driver

    def do_crawling(self, site_url):
        self.driver.get(site_url)
        return self.driver.page_source
