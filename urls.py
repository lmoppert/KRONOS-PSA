from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from .views import (ItemDetail, ItemList, CartDetail, EmptyCart,
                    RequisitionDetail)

urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)$', ItemDetail.as_view(), name='item_detail'),
    url(r'^category/(?P<pk>\d+)$', ItemList.as_view(), name='item_list'),
    url(r'^$', RedirectView.as_view(
        url=reverse_lazy('item_list', args=(3,))), name='psa_home'),
    url(r'^category/$', RedirectView.as_view(
        url=reverse_lazy('item_list', args=(3,)))),
    url(r'^cart/$', CartDetail.as_view(), name='cart_detail'),
    url(r'^cart/empty$', EmptyCart.as_view(), name='empty_cart'),
    url(r'^/$', CartDetail.as_view(), name='print_cart'),
    url(r'^requisition/(?P<pk>\d+)$', RequisitionDetail.as_view(),
        name='requisition_detail'),
)
