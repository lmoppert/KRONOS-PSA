from django.utils.translation import ugettext_lazy as _
from django import forms


class RequisitionForm(forms.Form):
    "Form for the Requisition"
    LOCATIONS = (('LEV', 'Leverkusen'), ('NHM', 'Nordenham'))
    name = forms.CharField(
        max_length=100,
        label=_("Name"),
        required=True,
    )
    location = forms.ChoiceField(
        choices=LOCATIONS,
        label=_("Location"),
        initial='LEV',
        required=True,
    )
    number = forms.CharField(
        max_length=100,
        label=_("Order Number"),
        required=True,
    )
    building = forms.CharField(
        max_length=100,
        label=_("Buildiing"),
        required=True,
    )
    phone = forms.CharField(
        max_length=100,
        label=_("Phone"),
        required=True,
    )
    fax = forms.CharField(
        max_length=100,
        label=_("FAX"),
        required=False,
    )
    email = forms.CharField(
        max_length=100,
        label=_("Email"),
        required=False,
    )
