# vim: set fileencoding=utf-8 :
"""Views for the psa shop."""

from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
# from django.http import HttpResponse, HttpResponseNotAllowed
from .forms import RequisitionForm
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

    def add_item(self, item, quantity):
        cart = self.get_or_create_cart(self.request.user)
        cartitem, created = cart.psaitems.get_or_create(item_id=item)
        if created:
            cartitem.quantity = int(quantity)
        else:
            cartitem.quantity += int(quantity)
        cartitem.save()
        return _("Items have been added to your cart")


class ItemListView(ItemMixin, ListView):
    "Generic View that adds the ItemMixin to the ListView"
    pass


class ItemDetailView(ItemMixin, DetailView):
    "Generic View that adds the ItemMixin to the DetailView"
    pass


class ItemDetail(FormMixin, ItemDetailView):
    context_object_name = "item"
    model = models.PSAProduct

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(
            active_id=self.object.category.parent_id,
        )
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        message = self.add_item(request.POST['item'], request.POST['quantity'])
        context = self.get_context_data(
            active_id=self.object.category.parent_id,
            message=message
        )
        return self.render_to_response(context)


class ItemList(ItemListView):
    model = models.PSAProduct
    flags = [True, False, False]

    def get_flags(self, request, location):
        if location == 'LEV':
            return [False, True, False]
        elif location == 'NHM':
            return [False, False, True]
        return [True, False, False]

    def get_location(self, request):
        if 'location' in request.GET:
            location = request.GET['location']
            request.session['location'] = location
            if location == 'All':
                del request.session['location']
        else:
            if 'location' in request.session:
                location = request.session['location']
            else:
                location = 'All'
        return location

    def get_queryset(self, location):
        qs = models.PSAProduct.objects.filter(category_id=self.kwargs['pk'])
        if not location == 'All':
            qs = qs.filter(Q(location=location) | Q(location='KRO'))
        return qs

    def get(self, request, *args, **kwargs):
        location = self.get_location(request)
        flags = self.get_flags(request, location)
        self.object_list = self.get_queryset(location)
        category = models.PSACategory.objects.get(pk=self.kwargs['pk'])
        context = self.get_context_data(
            category=category,
            active_id=category.parent_id,
            location=flags,
        )
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset(request)
        category = models.PSACategory.objects.get(pk=self.kwargs['pk'])
        message = self.add_item(request.POST['item'], request.POST['quantity'])
        context = self.get_context_data(
            category=category,
            active_id=category.parent_id,
            message=message
        )
        return self.render_to_response(context)


class CartDetail(FormMixin, ItemDetailView):
    model = models.PSACart
    context_object_name = 'cart'
    success_url = reverse_lazy('psa_home')

    def save_user_profile(self, user, data):
        profile = user.psaprofile
        profile.location = data.location
        profile.building = data.building
        profile.phone = data.phone
        profile.fax = data.fax
        profile.save()

    def get_empty_form(self, request):
        user = request.user
        profile, created = models.PSAProfile.objects.get_or_create(user=user)
        return RequisitionForm(initial={
            'name': user.get_full_name,
            'email': user.email,
            'location': profile.location,
            'building': profile.building,
            'phone': profile.phone,
            'fax': profile.fax,
        })

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
            processed=False).get_or_create(user=request.user)
        form = self.get_empty_form(request)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = request.user
        self.object = models.PSACart.objects.filter(
            processed=False).get(user=user)
        form = self.get_form(RequisitionForm)
        if form.is_valid():
            requisition = self.create_requisition(form)
            self.save_user_profile(user, requisition)
            cart = models.PSACart.objects.filter(processed=False).get(user=user)
            cart.processed = True
            cart.save()
            context = self.get_context_data(requisition=requisition,
                                            printed=True)
        elif "ch_item" in request.POST:
            item = self.object.psaitems.get(id=request.POST['ch_item'])
            item.quantity = int(request.POST['quantity'])
            item.save()
            context = self.get_context_data(form=self.get_empty_form(request))
        elif "rm_item" in request.POST:
            item = self.object.psaitems.get(id=request.POST['rm_item'])
            item.delete()
            context = self.get_context_data(form=self.get_empty_form(request))
        else:
            context = self.get_context_data(form=form, submitted=True)
        return self.render_to_response(context)


class EmptyCart(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        cart = models.PSACart.objects.filter(processed=False).get(user=user)
        cart.processed = True
        cart.save()
        return redirect(request.GET['ref'])


class RequisitionDetail(DetailView):
    model = models.PSARequisition
