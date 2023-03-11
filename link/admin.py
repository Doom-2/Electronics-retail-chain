from django.contrib import admin
from .models import Contact, ProductType, Product,  BusinessUnit, LegalPerson, Link
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html


@admin.action(description='Sets receivables value to 0 for selected objects')
def receivables_reset(modeladmin, request, queryset):
    queryset.update(receivables=0)


class LinkAdmin(admin.ModelAdmin):
    """
    Displays all fields except 'id'.
    Makes FKs 'legal_name' and 'supplier' as links.
    Allows to search and filter by field 'city' from 'Contact' model.
    Adds an action to reset the 'receivables' field.
    """

    list_display = ('title', 'legal_name_link', 'contact', 'products', 'supplier_set', 'receivables', 'created')
    list_filter = ('contact__city',)
    search_fields = ('contact__city',)
    actions = (receivables_reset,)

    def legal_name_link(self, obj: Link):
        link = reverse('admin:link_legalperson_change', args=[obj.legal_name.id])
        return format_html("<a href='{}'>{}</a>", link, obj.legal_name.title)

    legal_name_link.short_description = 'legal name'
    legal_name_link.admin_order_field = 'legal_name'

    def products(self, obj: Link):
        rel_list = "<div style=\"overflow: auto; height:80px;\"><ol style=\"PADDING-LEFT: 5px\">"
        for prod in obj.product.all():
            rel_list += '<li>%s</li>' % prod
        rel_list += '</ol></div>'
        return format_html(rel_list)

    def supplier_set(self, obj: Link):
        return self.links_to_objects(obj.legal_name.supplier.all())

    @classmethod
    def links_to_objects(cls, objects):
        rel_list = "<div style=\"overflow: auto; height:80px;\"><ol style=\"PADDING-LEFT: 5px\">"
        for obj in objects:
            link = reverse('admin:link_businessunit_change', args=[obj.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.title)
        rel_list += '</ol></div>'
        return format_html(rel_list)

    supplier_set.short_description = 'Suppliers'
    supplier_set.admin_order_field = 'legal_name__title'


admin.site.register(Contact)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(BusinessUnit)
admin.site.register(LegalPerson)
admin.site.register(Link, LinkAdmin)
admin.site.unregister(Group)
