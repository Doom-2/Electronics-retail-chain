from django.contrib import admin
from .models import Link, BusinessUnit, Product, Contact
from django.urls import reverse
from django.utils.html import format_html


@admin.action(description='Sets receivables value to 0 for selected objects')
def receivables_reset(modeladmin, request, queryset):
    queryset.update(receivables=0)


class LinkAdmin(admin.ModelAdmin):
    """
    Displays all fields except 'id'.
    Makes fk 'supplier' as link.
    Allows to search and filter by field 'city' from 'Contact' model.
    Adds an action to reset the 'receivables' field.
    """

    list_display = ('title', 'legal_name_link', 'contact', 'products', 'supplier_link', 'receivables', 'created')
    list_filter = ('contact__city',)
    search_fields = ('contact__city',)
    actions = (receivables_reset,)

    def legal_name_link(self, obj: Link):
        link = reverse('admin:link_businessunit_change', args=[obj.legal_name.id])
        return format_html("<a href='{}'>{}</a>", link, obj.legal_name.title)

    legal_name_link.short_description = 'legal name'
    legal_name_link.admin_order_field = 'legal_name'

    def supplier_link(self, obj: Link):
        link = reverse('admin:link_businessunit_change', args=[obj.supplier.id])
        return format_html("<a href='{}'>{}</a>", link, obj.supplier.title)

    supplier_link.short_description = 'Supplier'
    supplier_link.admin_order_field = 'legal_name__title'


admin.site.register(Link, LinkAdmin)
admin.site.register(BusinessUnit)
admin.site.register(Product)
admin.site.register(Contact)
