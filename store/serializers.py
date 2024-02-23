from decimal import Decimal
from rest_framework import serializers
from .models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
  class Meta:
    model= Collection
    fields=['id','title','products_count','featured_product']
  
  products_count = serializers.IntegerField(read_only=True)
  
  #featured_product = serializers.HyperlinkedRelatedField(
  #  queryset=Product.objects.all(),
  #  view_name='collection_products'
  #)





class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields=['id','title','description','slug','inventory','unit_price','unit_price_with_tax','collection']

  unit_price_with_tax=serializers.SerializerMethodField(method_name='calculated_Tax')

  #collection=serializers.PrimaryKeyRelatedField( queryset=Collection.objects.all() )
  #collection=serializers.StringRelatedField()
  #collection=CollectionSerializer()
  #collection = serializers.HyperlinkedRelatedField(
  #  queryset=Collection.objects.all(),
  #  view_name='collection_detail'
  #)
  
  def calculated_Tax(self,product:Product):
    return product.unit_price * Decimal(1.1)
