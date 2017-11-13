from django.conf.urls import url , include
from django.contrib import admin
from . import views


urlpatterns = [
	url(r'^$',views.index, name='index'),
	url(r'^login$', views.login_check, name='login'),
	url(r'^hostlist$', views.hostlist, name='hostlist'),
	url(r'^add$', views.add , name='add'),
	url(r'^edit/(\d+)$', views.edit, name='edit'),
	url(r'^editing/(\d+)$', views.editing, name='editing'),
	url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
	url(r'^useradd$', views.useradd, name='useradd'),
	url(r'^adduser$', views.adduser, name='adduser'),
	url(r'^saltcmd$', views.saltcmd, name='saltcmd'),
	url(r'^saltrun$', views.saltrun, name='saltrun'),

]