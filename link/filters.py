import django_filters
from .models import Link


class LinkModelFilter(django_filters.rest_framework.FilterSet):
    """
    Filters 'Link' queryset by specific value of 'country' field from 'Contact' model.
    """

    country = django_filters.CharFilter(field_name='contact__country', lookup_expr='icontains', )

    class Meta:
        model = Link
        fields = ('country', )
