from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^process/$', views.process_text, name = 'text-process'),
    url(r'^jason/$', views.jason, name = 'jason'),
    url(r'^kevin/$', views.kevin, name = 'kevin'),
    url(r'^charlie/$', views.charlie, name = 'charlie'),
    url(r'^jennifer/$', views.jennifer, name = 'jennifer')
]
