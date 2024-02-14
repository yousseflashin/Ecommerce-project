from decimal import Decimal
from rest_framework import serializers
from .models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
  class Meta:
    model= Collection
    fields=['id','title']




class ProductSerializer(serializers.Serializer):

  id = serializers.IntegerField()
  title = serializers.CharField(max_length=255)
  unit_price=serializers.DecimalField(max_digits=6,decimal_places=2)
  unit_price_with_tax=serializers.SerializerMethodField(method_name='calculated_Tax')

  #collection=serializers.PrimaryKeyRelatedField( queryset=Collection.objects.all() )
  #collection=serializers.StringRelatedField()
  #collection=CollectionSerializer()
  collection = serializers.HyperlinkedRelatedField(
    queryset=Collection.objects.all(),
    view_name='collection_detail'
  )
  def calculated_Tax(self,product:Product):
    return product.unit_price * Decimal(1.1)
