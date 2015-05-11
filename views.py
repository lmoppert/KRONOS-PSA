# vim: set fileencoding=utf-8 :
"""Views for the psa shop."""

from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
# from django import forms
from . import models


class ItemMixin(object):
    def get_or_create_cart(self, user):
        try:
            return models.PSACart.objects.filter(processed=False).get(user=user)
        except:
            return models.PSACart.objects.create(user=user)

    def get_context_data(self, **kwargs):
        context = super(ItemMixin, self).get_context_data(**kwargs)
        context['nodes'] = models.PSACategory.objects.filter(active=True)
        context['cart'] = self.get_or_create_cart(self.request.user)
        return context


class ItemListView(ItemMixin, ListView):
    pass


class ItemDetailView(ItemMixin, DetailView):
    pass


class ItemDetail(FormMixin, ItemDetailView):
    model = models.PSAProduct

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(
            active_id=self.object.category.parent_id,
        )
        return self.render_to_response(context)


class ItemList(FormMixin, ItemListView):
    model = models.PSAProduct

    def get_queryset(self):
        return models.PSAProduct.objects.filter(category_id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        category = models.PSACategory.objects.get(pk=self.kwargs['pk'])
        context = self.get_context_data(
            category=category,
            active_id=category.parent_id,
        )
        return self.render_to_response(context)


class CartDetail(FormMixin, ItemDetailView):
    model = models.PSACart
    context_object_name = 'cart'
    success_url = reverse_lazy('psa_home')

    def get_requisition(self, request):
        try:
            return models.PSARequisition.objects.filter(
                cart__processed=False).get(user=request.user)
        except:
            return models.PSARequisition.objects.new(user=request.user)

    def create_requisition(self, form):
        requisition = models.PSARequisition.objects.create(
            cart=self.object,
            name=form.cleaned_data['name'],
            building=form.cleaned_data['building'],
            phone=form.cleaned_data['phone'],
            fax=form.cleaned_data['fax'],
            number=form.cleaned_data['number'],
            email=form.cleaned_data['email'],
            location=form.cleaned_data['location'],
        )
        requisition.save()
        return requisition

    def get(self, request, *args, **kwargs):
        self.initial = models.PSARequisition.objects.create
        self.object = models.PSACart.objects.filter(
            processed=False).get(user=request.user)
        form = models.RequisitionForm(initial={
            'name': request.user.get_full_name,
            'email': request.user.email,
        })
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = models.PSACart.objects.filter(
            processed=False).get(user=request.user)
        form = self.get_form(models.RequisitionForm)
        context = self.get_context_data(form=form, submitted=True)
        if form.is_valid():
            requisition = self.create_requisition(form)
            return redirect(requisition)
        else:
            return self.render_to_response(context)


class RequisitionDetail(DetailView):
    model = models.PSARequisition
