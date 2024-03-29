from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from psa.models import PSACategory, PSAProduct


@admin.register(PSACategory)
class CategoryAdmin(MPTTModelAdmin, SortableModelAdmin):
    mptt_level_indent = 20
    list_display = ('name', 'description', 'active')
    list_filter = ('active', 'level')
    search_fields = ('name', 'description', 'teaser')
    sortable = 'order'
    actions = ('archive_categories', 'unarchive_categories')

    def activate_categories(self, request, queryset):
        queryset.update(active=True)
    activate_categories.short_description = _(
        "Activate selected categories")

    def deactivate_categories(self, request, queryset):
        queryset.update(active=False)
    deactivate_categories.short_description = _(
        "Deactivate selected categories")


@admin.register(PSAProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'active', 'location', 'category')
    list_filter = ('category', 'location', 'active')
    search_fields = ('name', 'number', 'description')
    actions = ('activate_items', 'deactivate_items')

    def activate_items(self, request, queryset):
        queryset.update(active=True)
    activate_items.short_description = _(
        "Activate selected items")

    def deactivate_items(self, request, queryset):
        queryset.update(active=False)
    deactivate_items.short_description = _(
        "Deactivate selected items")
