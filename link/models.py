from django.core.exceptions import ValidationError
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


class BusinessUnit(models.Model):
    class Meta:
        verbose_name = 'BusinessUnit'
        verbose_name_plural = 'BusinessUnits'

    class SupType(models.IntegerChoices):
        manufacturer = 0, 'Manufacturer'
        reseller = 1, 'Reseller'
        retailer = 2, 'Retailer'

    title = models.CharField(verbose_name='title', max_length=64)

    supplier = models.ForeignKey('self',
                                 on_delete=models.PROTECT,
                                 null=True, blank=True)

    type = PositiveSmallIntegerField(verbose_name='Supplier type',
                                     choices=SupType.choices,
                                     default=SupType.manufacturer)

    def __str__(self):
        return f'{self.title} ({self.get_type_display()})'

    def clean(self):
        """
        Checks the validity of the object hierarchy level
        and raises an exception before calling method save() if needed.
        """

        if self.supplier and self.type == self.SupType.manufacturer:
            raise ValidationError(
                'Top hierarchy level object cannot have a parent.'
            )
        elif not self.supplier and self.type != self.SupType.manufacturer:
            raise ValidationError(
                'Non-top hierarchy level object must have a parent.'
            )
        elif self.supplier and (
                self.supplier.type == self.SupType.retailer and self.type == self.SupType.reseller):
            raise ValidationError(
                'Object of a higher level cannot have a parent of a lower level.'
            )
        elif self.supplier and (
                self.supplier.type == self.SupType.reseller and self.type == self.SupType.reseller or
                self.supplier.type == self.SupType.retailer and self.type == self.SupType.retailer):
            raise ValidationError(
                'Object must have a parent of a higher level than itself.'
            )
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Link(DatesModelMixin):
    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    title = models.CharField(verbose_name='title', max_length=255, unique=True)
    legal_name = models.ForeignKey(BusinessUnit, verbose_name='legal_name', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact,
                                verbose_name='contact',
                                on_delete=models.PROTECT,
                                related_name='links', null=True, blank=True)
    product = models.ManyToManyField(Product, related_name='sellers', blank=True)
    receivables = models.DecimalField(verbose_name='receivables, RUB', max_digits=11, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def products(self):
        return ', '.join([str(p) for p in self.product.all()])

    @property
    def supplier(self):
        return self.legal_name.supplier if self.legal_name.supplier else self.legal_name

    def clean(self):
        """
        Checks the hierarchy level of the object referenced by the 'legal_name' field
        and prevents its creation if the type is 'Manufacturer'.
        """

        if self.legal_name.type == BusinessUnit.SupType.manufacturer:
            raise ValidationError(
                f'{self.legal_name.get_type_display()} cannot sell products. '
                f'Please, choose a non-top hierarchy level object.'
            )
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
