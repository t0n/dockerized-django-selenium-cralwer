from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    url(r'^$', views.HomePage.as_view(), name='home'),

    url('^login/$', auth_views.LoginView.as_view(template_name='login.html')),

    url(r'^dashboard/', include('apps.dashboard.urls', namespace='dashboard')),

]

# media files
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

