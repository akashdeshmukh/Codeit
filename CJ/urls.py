from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'CJ.views.my_custom_404_view'
handler500 = 'CJ.views.my_custom_error_view'
handler403 = 'CJ.views.my_custom_permission_denied_view'
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'CJ.views.home', name='home'),
    # url(r'^CJ/', include('CJ.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls')),
)
