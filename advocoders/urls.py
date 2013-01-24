from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import signals  # DO NOT REMOVE; register signals


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'advocoders.views.home', name='home'),
    url(r'^company/(?P<domain>([^/]*))$', 'advocoders.views.home', name='feed_company'),
    url(r'^company/(?P<domain>([^/]*))/(?P<provider>([^/]*))$', 'advocoders.views.home', name='feed_company_provider'),
    url(r'^logout$', 'advocoders.views.logout', name='logout'),
    url(r'^profile$', 'advocoders.views.profile', name='profile'),
    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
