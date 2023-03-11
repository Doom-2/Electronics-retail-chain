from rest_framework import serializers
from .models import Link, Product, BusinessUnit, Contact


class LinkCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):

    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='title'
    )

    supplier = serializers.SlugRelatedField(
        queryset=BusinessUnit.objects.all(),
        slug_field='title'
    )

    contact = serializers.SlugRelatedField(
        queryset=Contact.objects.all(),
        slug_field='country',
    )

    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ('receivables', )


class LinkUpdateSerializer(LinkSerializer):

    contact = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
    )
