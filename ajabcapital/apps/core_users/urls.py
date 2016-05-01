from django.conf.urls import include, url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name="dashboard"),

    url(r'^list/$', views.users, name="users"),
    # url(r'^roles/$', views.roles, name="roles"),

    url(r'^activate/$', views.activate_user, name="activate"),
    url(r'^deactivate/$', views.deactivate_user, name="deactivate"),

    url(r'^profile/view/$', views.view_profile, name="my-profile"),
    url(r'^profile/edit/$', views.edit_profile, name="edit-profile"),

    url(r'^password/change/$', views.password_change, name='password_change'),
    url(r'^password/forgot/$', views.password_reset, name='password_reset'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, name='password_reset_confirm'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'), 

]