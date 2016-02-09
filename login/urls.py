from django.conf.urls import include, url
from login import views
from django.conf import settings
from django.conf.urls.static import static
import login.views

urlpatterns = [
	url(r'^$', login.views.home_page,name='home'),	
        url(r'^login/$',login.views.login_page,name='login'),
        url(r'^logout/$',login.views.logout_page),
]