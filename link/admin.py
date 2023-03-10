from django.contrib import admin
from .models import Link, Supplier, Product, Contact


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

    list_display = ('title', 'contact', 'products', 'supplier', 'receivables', 'created')
    list_display_links = ('title', 'supplier',)
    list_filter = ('contact__city',)
    search_fields = ('contact__city',)
    actions = (receivables_reset,)


admin.site.register(Link, LinkAdmin)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Contact)
