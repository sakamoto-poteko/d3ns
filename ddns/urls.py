from django.urls import path
from . import views

urlpatterns = [
    path('', views.query_hosts_by_cred, name='query_hosts_index'),
    path('create_user', views.create_user, name='create_user'),
    path('query_hosts', views.query_hosts_by_cred, name='query_hosts'),
    path('host', views.query_ip_by_hostname, name='query_host'),
    path('nic/update', views.update_ip, name='update_ip'),
]