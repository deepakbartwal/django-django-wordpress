from django.conf.urls import url, include
from .views import *

urlpatterns = [
    # url(r'^test/', Test, name='test'),
    url(r'', Index, name='index'),
    # url(r'^login/', Login, name='login'),
    # url(r'^home/', Login, name='home'),
    # url(r'^/', Login, name='home'),
    # url(r'^(?P<k_type_slug>[-\w]+)/$', ServeTheme),
    # url(r'^$', ServeType, name='kitchen')
]
