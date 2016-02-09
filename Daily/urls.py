from django.conf.urls import include, url
from Daily import views

import Daily.views

urlpatterns = [
    url(r'^$',Daily.views.daily_page,name='daily'),
    url(r'^home/$',Daily.views.daily_page,name='daily_home'),
    url(r'^home_json/$',Daily.views.daily_page_json,name='daily_home_json'),
    url(r'^spec/(?P<date>\w+)/$',Daily.views.specific_day,name='specific_day'),
    url(r'^add_new/$',Daily.views.add_new,name='daily_add'),
]