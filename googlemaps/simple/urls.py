from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^process/$', views.process_text, name = 'text-process'),
    url(r'^jason/$', views.jason, name = 'jason'),
    url(r'^kevin/$', views.kevin, name = 'kevin'),
    url(r'^charlie/$', views.charlie, name = 'charlie'),
    url(r'^jennifer/$', views.jennifer, name = 'jennifer'),
    url(r'^celine/$', views.celine, name = 'celine'),
    url(r'^montrealgazette/$', views.montreal_gazette, name = 'montreal-gazette'),
    url(r'^montrealgazette/(?P<slug>.*)/$', views.view_montreal_gazette, name = 'view-montreal-gazette'),
    url(r'^processgazette/$', views.process_gazette, name = 'process-gazette')
]
