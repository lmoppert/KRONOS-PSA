from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from psa.models import PSACategory, PSAProduct


@admin.register(PSACategory)
class CategoryAdmin(MPTTModelAdmin, SortableModelAdmin):
    mptt_level_indent = 20
    list_display = ('name', 'description', 'active')
    list_filter = ('active', )
    search_fields = ('name', 'description', 'teaser')
    sortable = 'order'
    actions = ('archive_categories', 'unarchive_categories')

    def archive_categories(self, request, queryset):
        queryset.update(active=True)
    archive_categories.short_description = _(
        "Move selected categories to archive")

    def unarchive_categories(self, request, queryset):
        queryset.update(active=False)
    unarchive_categories.short_description = _(
        "Remove selected categories from archive")


@admin.register(PSAProduct)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'active', 'location', 'category')
    list_filter = ('category', 'location', 'active')
    search_fields = ('name', 'number', 'description')
    actions = ('archive_items', 'unarchive_items')

    def archive_items(self, request, queryset):
        queryset.update(active=True)
    archive_items.short_description = _(
        "Move selected items to archive")

    def unarchive_items(self, request, queryset):
        queryset.update(active=False)
    unarchive_items.short_description = _(
        "Remove selected items from archive")
