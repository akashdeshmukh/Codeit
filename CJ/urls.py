from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'CJ.views.my_custom_404_view'
handler500 = 'CJ.views.my_custom_error_view'
handler403 = 'CJ.views.my_custom_permission_denied_view'
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'codeit.views.index', name='index'),
    url(r'^home/$', 'codeit.views.home', name='home'),
    url(r'^logout/$', 'codeit.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls')),
)
