from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .signals import order_created
from .models import Collection, Order, OrderItem, Product, ProductImage,Review,Cart,CartItem,Customer

class ProductImageSerializer(serializers.ModelSerializer):
  def create(self,validated_data):
    product_id=self.context['product_id']
    return ProductImage.objects.create(product_id=product_id,**validated_data)
  
  class Meta:
    model=ProductImage
    fields=['id','image']
    


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
  images = ProductImageSerializer(many=True,read_only=True)
  class Meta:
    model = Product
    fields=['id','title','description','slug','inventory','unit_price','unit_price_with_tax','collection','images']

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




class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields=['id','date','name','description','product']



class SimpleProduct(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields=['id','title','unit_price']



class CartItemSeralizer(serializers.ModelSerializer):
  class Meta:
    model = CartItem
    fields=['id','product','quantity','total_price']
  
  product = SimpleProduct(read_only=True)
  total_price=serializers.SerializerMethodField(method_name='total_item_price')

  def total_item_price(self,cart_item:CartItem):
      return cart_item.quantity * cart_item.product.unit_price
  
class UpdateCartItemSerializer(serializers.ModelSerializer):
  class Meta:
    model=CartItem
    fields=['quantity']

  
class AddCartItemSerializer(serializers.ModelSerializer):
  class Meta:
    model=CartItem
    fields=['id','product_id','quantity']
  
  product_id=serializers.IntegerField()
  
  def validate_product_id(self,value):
    if not Product.objects.filter(pk=value).exists():
        raise serializers.ValidationError('No product withe the id given')
    return value
  def save(self, **kwargs):
    cart_id = self.context['cart_id']
    product_id = self.validated_data['product_id']
    quantity = self.validated_data['quantity']

    try:
     
     cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
     cart_item.quantity += quantity
     cart_item.save()
     self.instance=cart_item

    except CartItem.DoesNotExist:

      self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data) 

    return self.instance
  

class CartSeralizer(serializers.ModelSerializer):
  
  class Meta:
    model = Cart
    fields=['id','items_numbers','cartitem_set','total_price']


  id = serializers.UUIDField(read_only=True)
  cartitem_set=CartItemSeralizer(many=True,read_only=True)
  total_price = serializers.SerializerMethodField(method_name='cart_total_price')
  items_numbers = serializers.SerializerMethodField(method_name='cart_items_number')
   
  def cart_total_price(self,cart:Cart):
    total=0
    for item in cart.cartitem_set.all():
       total+=(item.quantity * item.product.unit_price)
    return total 
  
  def cart_items_number(self,cart:Cart):
    total=0
    for item in cart.cartitem_set.all():
       total+=item.quantity 
    return total 


class CustomerSeralizer(serializers.ModelSerializer):
  user_id = serializers.IntegerField(read_only=True)
  class Meta:
    model=Customer
    fields=['id','user_id','phone','birth_date','membership']

class OrderItemSerializers(serializers.ModelSerializer):
  product=SimpleProduct()
  class Meta:
    model = OrderItem
    fields=['id','product','order','unit_price','quantity']

class OrderSerializers(serializers.ModelSerializer):
  items = OrderItemSerializers(many=True)
  class Meta:
    model = Order
    fields = ['id','customer','placed_at','payment_status','items']


class UpdateOrderSerializer(serializers.ModelSerializer):
  class Meta:
    model=Order
    fields=['payment_status']


class CreateOrderSerializer(serializers.Serializer):
  cart_id=serializers.UUIDField()
  def validate_cart_id(self,cart_id):
      if not Cart.objects.filter(pk=cart_id).exists():
        raise serializers.ValidationError('No cart with the given ID was found')
      if CartItem.objects.filter(cart_id=cart_id).count()==0:
        raise serializers.ValidationError('the cart is empty')
      return cart_id
  def save(self,**kwargs):
      cart_id=self.validated_data['cart_id']
      with transaction.atomic():
      
        customer=Customer.objects.get(user_id=self.context['user_id'])
        order=Order.objects.create(customer=customer)
        

        cart_items=CartItem.objects\
        .select_related('product')\
          .filter(cart_id=cart_id)
        
        order_items = [OrderItem(
          order=order,
          product=item.product,
          unit_price=item.product.unit_price,
          quantity=item.quantity,
        )for item in cart_items]
        OrderItem.objects.bulk_create(order_items)

        Cart.objects.filter(pk=cart_id).delete()

        order_created.send_robust( self.__class__,order=order)

      return Order
       