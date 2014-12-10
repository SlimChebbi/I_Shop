from django.conf.urls import patterns, include, url
urlpatterns = patterns('reparations.views',
                       url(r'^terminer$', 'terminer',
                           name='terminer'),
                       url(r'^encour$', 'encour',
                           name='encour'),

                       url(r'^add_reparation/(?P<id>\d+)/$', 'add_reparation',
                           name='add_reparation'),

                       url(r'^add_facture/(?P<id>\d+)/$', 'add_facture',
                           name='add_facture'),

                       url(r'^add_mainouvre/(?P<id>\d+)/$', 'add_mainouvre',
                           name='add_mainouvre')
                       ,
                       url(r'^delete_reparation/(?P<id>\d+)/$',
                           'delete_reparation',
                           name='delete_reparation'),

                       url(r'^edite_reparation/(?P<id>\d+)/$',
                           'edite_reparation',
                           name='edite_reparation'),

                       url(r'^reparation/(?P<id>\d+)/$', 'reparation',
                           name='reparation'),

                       url(r'^change_status/(?P<id>\d+)/$', 'change_status',
                           name='change_status'),


                       url(r'^delete_piece/(?P<id>\d+)/$',
                           'delete_piece',
                           name='delete_piece'),

                       url(r'^edite_piece/(?P<id>\d+)/$',
                           'edite_piece',
                           name='edite_piece'),

                       url(r'^delete_main/(?P<id>\d+)/$',
                           'delete_main',
                           name='delete_main'),

                       url(r'^edite_main/(?P<id>\d+)/$',
                           'edite_main',
                           name='edite_main'),

                       url(r'^paye/(?P<id>\d+)/$',
                           'paye',
                           name='paye'),
                       )
