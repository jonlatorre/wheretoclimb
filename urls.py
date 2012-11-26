from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
#    url(r"^$", direct_to_template, {
#        "template": "homepage.html",
#    }, name="home"),
    url(r"^$", redirect_to, {'url':'/crags/'}, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r'^crags/', include('crags.urls')),
    url(r'^topos/', include('topos.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    #for the maps with gmapi
    url(r'', include('gmapi.urls.media')),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
                                (r'^%s(?P<path>.*)$' % _media_url,
                                serve,
                                {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)
