from django.conf.urls import url

from . import views

app_name = 'andablog'
urlpatterns = [
    url('^$', views.EntriesList.as_view(), name='entrylist'),
    url(r'^entry_add/$', views.EntryAdd, name='entryadd'),
    url(r'^entry_create/$',views.EntryCreate.as_view(),name='entrycreate'),
    url(r'^entry_update/(?P<slug>[A-Za-z0-9-_]+)/$',views.EntryUpdate.as_view(),name='entryupdate'),
    url(r'^entry_delete/(?P<slug>[A-Za-z0-9-_]+)/$',views.EntryDelete.as_view(),name='entrydelete'),
    url(r'^detail/(?P<slug>[A-Za-z0-9-_]+)/$', views.EntryDetail.as_view(), name='entrydetail'),
    url(r'^unpublished$', views.EntriesListUnpublished.as_view(), name='entrylistunpublished'),
    url(r'^unpublished/detail/(?P<slug>[A-Za-z0-9-_]+)/$', views.EntryDetailUnpublished.as_view(), name='entrydetailunpublished'),
]