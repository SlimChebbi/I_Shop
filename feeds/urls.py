from django.conf.urls import patterns, include, url

urlpatterns = patterns('feeds.views',
                       url(r'^$', 'feeds', name='feeds'),
                       url(r'^post/$', 'post', name='post'),

                       url(r'^load/$', 'load', name='load'),
                       url(r'^check/$', 'check', name='check'),
                       url(r'^load_new/$', 'load_new', name='load_new'),



                       url(r'^(\d+)/$', 'feed', name='feed'),
                       )
