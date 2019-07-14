from django.conf.urls import url
#from .views import Index
from . import views

urlpatterns = [
    url(r'^$', views.show_employees, name='show_employees'),
    url(r'^employees$', views.show_employees, name='show_employees'),
    url(r'^change_boss/$', views.change_boss, name='change_boss'),
    url(r'^employees_all/$', views.show_employees_all, name='show_employees_all'),
    url(r'^edit/(?P<id>\d+)/', views.edit, name='edit'),
    url(r'^delete/(?P<id>\d+)/', views.delete, name='delete'),
]
