from django.conf.urls import patterns, include, url
urlpatterns = patterns('lignes.views',


                       url(r'^add_ligne/(?P<id>\d+)/$', 'add_ligne',
                           name='add_ligne'),
                       url(r'^vendre_ligne/(?P<type>\d+)/(?P<id>\d+)/$',
                           'vendre_ligne', name='vendre_ligne'),

                       url(r'^vendreligne/(?P<id>\d+)/$',
                           'vendreligne', name='vendreligne'),
                       url(r'^ligne/(?P<id>\d+)/$', 'ligne',
                           name='ligne'),
                       url(r'^ooredoo$', 'ooredoo',
                           name='ooredoo'),
                       url(r'^orange$', 'orange',
                           name='orange'),


                       url(r'^telecom$', 'telecom',
                           name='telecom'),

                       url(r'^delete_ligne/(?P<id>\d+)/(?P<type>\d+)/$',
                           'delete_ligne',
                           name='delete_ligne'),
                       url(r'^edite_ligne/(?P<id>\d+)/(?P<type>\d+)/$',
                           'edite_ligne',
                           name='edite_ligne'),


                       )
