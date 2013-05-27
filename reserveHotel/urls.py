from django.conf.urls import patterns, url
from reserveHotel import views


urlpatterns = patterns('',
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.log_in, name = 'login'),
    url(r'^searchHotel/$', views.search_hotel, name = 'searchHotel'),
    url(r'^searchResult/$', views.search_result, name = 'searchResult'),
    url(r'^chooseRoom/$', views.choose_room, name = 'chooseRoom'),
    url(r'^roomConfirm/$', views.room_confirm, name = 'roomConfirm'),
    url(r'^payment/&', views.payment, name = 'payment'),
)