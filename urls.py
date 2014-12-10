from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:portables
                       # url(r'^$', 'I_Shop.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       # url(r'^accessoires/',
                       #     include('I_Shop.accessoires.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', include('home.urls')),
                       url(r'^feeds/', include('feeds.urls')),
                       url(r'^reports/', include('reports.urls')),
                       url(r'^accessoires/', include('accessoires.urls')),
                       url(r'^portables/', include('portables.urls')),
                       url(r'^lignes/', include('lignes.urls')),
                       url(r'^reparations/', include('reparations.urls')),
                       url(r'^login', 'django.contrib.auth.views.login',
                           {'template_name': 'home/login.html'}, name='login'),
                       url(r'^logout', 'django.contrib.auth.views.logout',
                           {'next_page': '/'}, name='logout'),




                       )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
