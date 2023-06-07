from rest_framework import serializers
from .models import Products, Categories


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Categories
        fields = ('id', 'name', 'supercategory')


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Products
        fields = ('id', 'name', 'category', 'weight', 'description',
                  'composition', 'storage_conditions', 'number', 'price', 'status')
