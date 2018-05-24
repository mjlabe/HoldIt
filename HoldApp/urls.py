from django.conf.urls import url
from HoldApp.views import views_public, views_user, views_contrib
from django.urls import path, include


urlpatterns = [
    url(r'^case/new/H$', views_contrib.new_case, name='new_case'),
    url(r'^case/new/D$', views_contrib.new_Dcase, name='new_Dcase'),
    url(r'^$', views_public.index, name='index'),
    url(r'^$', views_public.header, name='header'),
    url(r'^$', views_public.footer, name='footer'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^registration/signup/$', views_public.signup, name='signup'),
    url(r'^registration/success/$', views_public.success, name='success'),
    url(r'^cases/recent/$', views_user.case_list, name='case_list'),
    url(r'^case/(?P<pk>\d+)/$', views_user.case_detail, name='case_detail'),
    url(r'^case/(?P<pk>\d+)/edit/$', views_contrib.case_edit, name='case_edit'),

]
