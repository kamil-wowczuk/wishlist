from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^dashboard$', dashboard),
    url(r'^login$', login),
    url(r'^logout$', logout),
    url(r'^register$', register),
    url(r'^wish_items/(?P<product_id>\d+)$', wish_items),
    url(r'^create$', create),
    url(r'^add_product$', add_product),
    url(r'^add/(?P<product_id>\d+)$', add),
    url(r'^remove/(?P<product_id>\d+)$', remove),
    url(r'^delete/(?P<product_id>\d+)$', delete),
]