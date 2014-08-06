from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('snisi_web.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

handler400 = 'snisi_web.views.errors.bad_request'
handler403 = 'snisi_web.views.errors.permission_denied'
handler404 = 'snisi_web.views.errors.not_found'
handler500 = 'snisi_web.views.errors.server_error'
