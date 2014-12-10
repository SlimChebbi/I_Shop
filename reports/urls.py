from django.conf.urls import patterns, include, url


urlpatterns = patterns('reports.views',


                       # url(r'^informatique/login/$',
                       #     'loginUser', name='login'),
                       url(r'^all$', 'all',
                           name='all'),
                       url(r'^now$', 'now',
                           name='now'),
                       url(r'^mois$', 'mois',
                           name='mois'),
                       url(r'^year$', 'year',
                           name='year'),
                       url(r'^semain$', 'semain',
                           name='semain'),

                       url(r'^delete_vendre/(?P<id>\d+)/$',
                           'delete_vendre',
                           name='delete_vendre'),

                       )
