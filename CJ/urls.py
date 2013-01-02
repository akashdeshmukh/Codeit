from django.conf.urls import patterns, include, url
from django.contrib import admin


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
    url(r'^logout/$', 'codeit.views.logout', name='logout'),
    url(r'^ranking/$', 'codeit.views.ranking', name='ranking'),
    url(r'^problem/(?P<problem_id>\d+)/$', 'codeit.views.problem', name='problem'),
    url(r'^solution/(?P<problem_id>\d+)/$', 'codeit.views.solution', name='solution'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/$', 'blog.views.index'),
    url(r'^blog/(?P<post_id>\d+)/$', 'blog.views.detail'),
)
