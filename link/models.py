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


class ProductType(models.Model):
    class Meta:
        verbose_name = 'ProductType'
        verbose_name_plural = 'ProductsTypes'

    title = models.CharField(verbose_name='title', max_length=64, unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    title = models.CharField(max_length=255)
    type = models.ForeignKey(ProductType, related_name='devices', on_delete=models.CASCADE, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True, unique=True)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.model}'


class BusinessUnit(models.Model):
    class Meta:
        verbose_name = 'BusinessUnit'
        verbose_name_plural = 'BusinessUnits'

    class BUType(models.IntegerChoices):
        manufacturer = 0, 'Manufacturer'
        reseller = 1, 'Reseller'
        retailer = 2, 'Retailer'

    title = models.CharField(verbose_name='title', max_length=64)

    type = PositiveSmallIntegerField(verbose_name='Business unit type',
                                     choices=BUType.choices,
                                     default=BUType.manufacturer)

    def __str__(self):
        return f'{self.title} ({self.get_type_display()})'


class LegalPerson(models.Model):
    class Meta:
        verbose_name = 'Legal Person'
        verbose_name_plural = 'Legal Persons'

    title = models.CharField(verbose_name='title', max_length=255, unique=True)
    supplier = models.ManyToManyField(BusinessUnit, verbose_name='supplier(s)', related_name='sellers', blank=True)

    def __str__(self):
        return self.title


class Link(DatesModelMixin):
    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    title = models.CharField(verbose_name='title', max_length=255)
    legal_name = models.ForeignKey(LegalPerson, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey(Contact,
                                verbose_name='contact',
                                on_delete=models.PROTECT,
                                related_name='links', null=True, blank=True)
    product = models.ManyToManyField(Product, verbose_name='product(s)', related_name='sellers', blank=True)
    receivables = models.DecimalField(verbose_name='receivables, RUB', max_digits=11, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    # @property
    # def suppliers(self):
    #     """
    #     Returns list of  LegalPerson object suppliers as string, separated by comma
    #     """
    #     return ', '.join([str(p) for p in self.legal_name.supplier.all()])\
    #         if self.legal_name.supplier.all() else 'N/A'
