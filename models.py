from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey


class PSAProfile(models.Model):
    "Class that adds some fields to the user class"

    LOCATIONS = (('LEV', 'Leverkusen'), ('NHM', 'Nordenham'))
    user = models.OneToOneField(User, verbose_name=_("PSAProfile"))
    location = models.CharField(max_length=3, choices=LOCATIONS, default="KRO",
                                verbose_name=_("Location"), null=True)
    building = models.CharField(max_length=100, verbose_name=_("Building"),
                                null=True)
    phone = models.CharField(max_length=100, verbose_name=_("Phone"), null=True)
    fax = models.CharField(max_length=100, verbose_name=_("FAX"), null=True)


class PSACategory(MPTTModel):
    "Class for categorisation of PSA items."

    name = models.CharField(max_length=200, verbose_name=_("Category"))
    description = models.TextField(blank=True, default='',
                                   verbose_name=_("Description"))
    teaser = models.TextField(blank=True, default='', verbose_name=_("Teaser"))
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)
    order = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('item_list', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    class MPTTMeta:
        order_insertion_by = ['order']

    def save(self, *args, **kwargs):
        super(PSACategory, self).save(*args, **kwargs)
        PSACategory.objects.rebuild()


class PSAProduct(models.Model):
    "Class defining a shop item"
    LOCATIONS = (('KRO', 'KRONOS'), ('LEV', 'Leverkusen'), ('NHM', 'Nordenham'))

    name = models.CharField(max_length=200, verbose_name=_("PSA Item"))
    number = models.CharField(max_length=50, verbose_name=_("Article Number"))
    description = models.TextField(blank=True, default='',
                                   verbose_name=_("Description"))
    image = FilerImageField(null=True, blank=True, verbose_name=_("Image"))
    location = models.CharField(max_length=3, choices=LOCATIONS, default="KRO",
                                verbose_name=_("Location"))
    category = models.ForeignKey(PSACategory, verbose_name=_("Category"))
    active = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"{} - {} ({})".format(self.number, self.name, self.location)

    class Meta:
        ordering = ('number', )
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")


class PSACart(models.Model):
    "Class mapping Items to a Cart"
    user = models.ForeignKey(User, verbose_name=_("User"))
    processed = models.BooleanField(default=False, verbose_name=_("Processed"))


class PSACartItems(models.Model):
    "Class mapping Items to a Cart"
    item = models.ForeignKey(PSAProduct, verbose_name=_("PSA Item"))
    cart = models.ForeignKey(PSACart, verbose_name=_("PSA Cart"),
                             related_name="psaitems")
    quantity = models.IntegerField(verbose_name=_("Quantity"), default=1)


class PSARequisition(models.Model):
    "Class for collection PSA items"
    LOCATIONS = (('LEV', 'Leverkusen'), ('NHM', 'Nordenham'))
    cart = models.ForeignKey(PSACart, verbose_name=_("PSA Cart"))
    name = models.CharField(max_length=100, verbose_name=_("Building"))
    building = models.CharField(max_length=100, verbose_name=_("Building"))
    phone = models.CharField(max_length=100, verbose_name=_("Phone"))
    fax = models.CharField(max_length=100, verbose_name=_("FAX"), null=True)
    number = models.CharField(max_length=100, verbose_name=_("Order Number"))
    email = models.CharField(max_length=100, verbose_name=_("Order Number"),
                             null=True)
    location = models.CharField(max_length=3, choices=LOCATIONS, default="KRO",
                                verbose_name=_("Location"))

    def get_absolute_url(self):
        return reverse('requisition_detail', kwargs={'pk': self.pk})
