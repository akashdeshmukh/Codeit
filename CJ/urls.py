from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Discover admin
admin.autodiscover()

# Define handlers for errors
handler404 = 'CJ.views.my_custom_404_view'
handler500 = 'CJ.views.my_custom_error_view'
handler403 = 'CJ.views.my_custom_permission_denied_view'

# Url mapping
urlpatterns = patterns('',
    url(r'^$', 'codeit.views.index', name='index'),
    url(r'^home/$', 'codeit.views.home', name='home'),
    url(r'^contact/$', 'codeit.views.contact', name='contact'),
    url(r'^about/$', 'codeit.views.about', name='about'),
    url(r'^logout/$', 'codeit.views.logout', name='logout'),
    url(r'^ranking/$', 'codeit.views.ranking', name='ranking'),
    url(r'^demo/$', 'codeit.views.demo', name='demo'),
    url(r'^problem/(?P<problem_id>\d+)/$', 'codeit.views.problem', name='problem'),
    url(r'^solution/(?P<problem_id>\d+)/$', 'codeit.views.solution', name='solution'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/$', 'codeit.blogviews.blogindex', name='blogindex'),
    url(r'^blog/(?P<post_id>\d+)/$', 'codeit.blogviews.blogdetail', name='blogdetail'),
)
urlpatterns += staticfiles_urlpatterns()
