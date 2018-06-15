from django.conf.urls import url
from HoldApp.views import views_public, views_user, views_contrib, OrderListJson, views_worker, views_admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from HoldApp.views.views_user import CaseView


urlpatterns = [
    url(r'^case/new/H$', views_contrib.new_case, name='new_case'),
    url(r'^packet/new/$', views_contrib.new_packet, name='new_packet'),
    url(r'^packetcasething/(?P<pk>\d+)/edit/$', views_contrib.edit_packet, name='edit_packet'),
    url(r'^packet/(?P<pk>\d+)/$', views_worker.packet_detail, name='packet_detail'),
    url(r'^packetsassigned/$', views_worker.packet_list_assigned, name='packet_list_assigned'),
    url(r'^packetqueue/$', views_worker.packet_list_queue, name='packet_list_queue'),
    url(r'^packet/(?P<pk>\d+)/edit/$', views_worker.packet_edit, name='packet_edit'),
    url(r'^case/new/D$', views_contrib.new_Dcase, name='new_Dcase'),
    url(r'^$', views_public.index, name='index'),
    url(r'^$', views_public.header, name='header'),
    url(r'^$', views_public.footer, name='footer'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^registration/signup/$', views_public.signup, name='signup'),
    url(r'^registration/success/$', views_public.success, name='success'),
    url(r'^cases/recent/$', views_user.case_list, name='case_list'),
    # url(r'^case/(?P<pk>\d+)/$', views_user.case_detail, name='case_detail'),
    url(r'^case/(?P<pk>\d+)/$', CaseView.as_view(), name='case_detail'),
    url(r'^case/(?P<pk>\d+)/edit/$', views_contrib.case_edit, name='case_edit'),
    url(r'^my/datatable/data/$', login_required(OrderListJson.as_view()), name='order_list_json'),
    # path('about/', CaseView.as_view(greeting="G'day")),
    url(r'^metrics/$', views_admin.metrics, name='metrics'),

]
