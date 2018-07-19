from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^accounts/profile/$', views.my_account, name='my_account'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^product_cart/$', views.product_cart, name='product_cart'),
    url(r'^product_wishlist/$', views.product_wishlist, name='product_wishlist'),
    url(r'^product/(?P<pk>\d+)/$', views.product_single, name='product_single'),
    url(r'^product_shop/$', views.product_shop, name='product_shop'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^add_to_cart/$', views.add_to_cart, name='add_to_cart'),
    url(r'^delete_from_cart/$', views.delete_from_cart, name='delete_from_cart'),
    url(r'^changing_quanity/$', views.changing_quanity, name='changing_quanity'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]
