from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    url(r'^$', views.HomePage.as_view(), name='home'),

    url(r'^sites/create$', views.SiteConfigurationCreateView.as_view(), name='sites_create'),

    url(r'^crawling/start$', views.StartCrawling.as_view(), name='start_crawling'),


]

# media files
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

