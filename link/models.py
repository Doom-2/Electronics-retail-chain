from django.db import models
from django.db.models import PositiveSmallIntegerField
from django.utils.translation import gettext_lazy as _


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True  # prevents table creation for this model

    created = models.DateTimeField(verbose_name='created at', auto_now_add=True)


class Contact(models.Model):
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    email = models.EmailField(_('email address'), null=True, blank=True, unique=True)
    country = models.CharField(_('country'), null=True, blank=True, max_length=32)
    city = models.CharField(_('city'), null=True, blank=True, max_length=32)
    street = models.CharField(_('street'), null=True, blank=True, max_length=32)
    bld_num = models.CharField(_('building number'), null=True, blank=True, max_length=8)

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street}, {self.bld_num}'


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    title = models.CharField(verbose_name='title', max_length=255)
    model = models.CharField(verbose_name='model', max_length=255, null=True, blank=True)
    release_date = models.DateField(verbose_name='release date', null=True, blank=True)

    def __str__(self):
        return self.title


class Supplier(models.Model):
    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    class SupType(models.IntegerChoices):
        manufacturer = 0, 'Manufacturer'
        reseller = 1, 'Reseller'
        retailer = 2, 'Retailer'

    title = models.CharField(verbose_name='title', max_length=64)

    supplier_parent = models.ForeignKey('self',
                                        on_delete=models.PROTECT,
                                        null=True, blank=True)

    type = PositiveSmallIntegerField(verbose_name='Supplier type',
                                     choices=SupType.choices,
                                     default=SupType.manufacturer)

    def __str__(self):
        return self.title


class Link(DatesModelMixin):
    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    title = models.CharField(verbose_name='title', max_length=255, unique=True)
    contact = models.ForeignKey(Contact,
                                verbose_name='contact',
                                on_delete=models.PROTECT,
                                related_name='links', null=True, blank=True)
    product = models.ManyToManyField(Product, related_name='sellers', blank=True)
    supplier = models.ForeignKey(Supplier,
                                 verbose_name='supplier',
                                 on_delete=models.PROTECT,
                                 related_name='distributors', null=True, blank=True)
    receivables = models.DecimalField(verbose_name='receivables, RUB', max_digits=11, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def products(self):
        return ', '.join([str(p) for p in self.product.all()])
