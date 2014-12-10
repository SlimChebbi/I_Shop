from django.conf.urls import patterns, include, url


urlpatterns = patterns('accessoires.views',


                       # url(r'^informatique/login/$',
                       #     'loginUser', name='login'),
                       url(r'^informatique$', 'informatique',
                           name='informatique'),


                       url(r'^portable$', 'portable',
                           name='portable'),

                       url(r'^accessoire/(?P<id>\d+)/$', 'accessoire',
                           name='accessoire'),

                       url(r'^vendre/(?P<id>\d+)/$', 'vendre',
                           name='vendre'),

                       url(r'^add_accessoire/(?P<id>\d+)/$', 'add_accessoire',
                           name='add_accessoire'),

                       url(r'^delete_accessoire/(?P<id>\d+)/(?P<type>\d+)/$',
                           'delete_accessoire',
                           name='delete_accessoire'),

                       url(r'^edite_accessoire/(?P<id>\d+)/(?P<type>\d+)/$',
                           'edite_accessoire',
                           name='edite_accessoire'),

                       url(r'^vendre_accessoire/(?P<type>\d+)/(?P<id>\d+)/$',
                           'vendre_accessoire', name='vendre_accessoire'),

                       )
