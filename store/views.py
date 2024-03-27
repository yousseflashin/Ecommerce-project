from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
from rest_framework.decorators import action
from rest_framework import response,decorators,status
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin

from .permission import ISAdminOrReadOnly, ViewCustomerHistoryPermission
from .filters import ProductFilter
from .models import Cart, Collection, Order, Product,OrderItem,Review,CartItem,Customer
from .serializers import CreateOrderSerializer, CustomerSeralizer, OrderSerializers, ProductSerializer,CollectionSerializer,ReviewSerializer,CartSeralizer,AddCartItemSerializer,CartItemSeralizer,UpdateCartItemSerializer, UpdateOrderSerializer
from .pagination import DefaultPagination
# Create your views here.


class ProductViewSet(ModelViewSet):
    
    queryset= Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    permission_classes = [ISAdminOrReadOnly]
    filterset_class=ProductFilter
    pagination_class=DefaultPagination
    search_fields=['title','description','collection__title']
    ordering_fields = ['unit_price','last_update']
    def get_serializer_context(self):
      return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):

      if OrderItem.objects.filter(Product_id=kwargs['pk']).count() > 0:
      
         return response.Response({'error':'product cannot be deleted because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      return super().destroy(request, *args, **kwargs)
    
   

class CollectionViewSet(ModelViewSet):
   
  queryset=Collection.objects.select_related('featured_product').annotate(products_count=Count('product')).all()
  serializer_class=CollectionSerializer
  permission_classes = [ISAdminOrReadOnly]
  
  def get_serializer_context(self):
      return {'request': self.request}

  def delete(self,request,pk):
    collections=get_object_or_404(Collection.objects.annotate(products_count=Count('product')),pk=pk)
    if Collection.product.count() > 0:
        return response.Response({'error':'product cannot be deleted because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    collections.delete()
    return response.Response(status=status.HTTP_204_NO_CONTENT)



@decorators.api_view()
def collection_products(request,pk):
  
  products=Product.objects.filter(id=pk)
  serializer=ProductSerializer(products,many=True,context={'request': request})
  return response.Response(serializer.data)


class ReviewViewSet(ModelViewSet):
   queryset=Review.objects.all()
   serializer_class = ReviewSerializer


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
   queryset = Cart.objects.prefetch_related('cartitem_set__product').all()
   serializer_class = CartSeralizer



class CartItemViewSet(ModelViewSet):
   
   http_method_names =['get','delete','patch','post']
   def get_serializer_class(self):
      if self.request.method == 'POST':
         return AddCartItemSerializer
      elif self.request.method =='PATCH':
         return UpdateCartItemSerializer
      return CartItemSeralizer
    

   def get_serializer_context(self):
       return {'cart_id':self.kwargs['cart_pk']}
   

   def get_queryset(self):
      return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')



class CustomerViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
   queryset =  Customer.objects.all()
   serializer_class = CustomerSeralizer
   permission_classes = [DjangoModelPermissions]
   def get_permissions(self):
      if self.request.method == 'GET':
        return [AllowAny()]
      return [IsAuthenticated()]
   
   @action(detail=True,permission_classes=[ViewCustomerHistoryPermission])
   def history(self,request,pk):
      return response.Response('ok')
   @action(detail=False,methods=['GET','PUT'])
   def me(self,request):
      customer=Customer.objects.get(user_id=request.user.id)
      if request.method =='GET':
         serializer = CustomerSeralizer(customer)
         return response.Response(serializer.data)
      elif request.method=='PUT':
         serializer = CustomerSeralizer(customer,data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return response.Response(serializer.data)
      

class OrderViewSet(ModelViewSet):
   http_method_names=['get','post','patch','delete','head','options']
   def get_permissions(self):
      if self.request.method in ['PATCH','DELETE']:
         return [IsAdminUser()]
      return [IsAuthenticated()]

   def create(self,request,*args,**kwargs):
      serializer=CreateOrderSerializer(data=request.data,context={'user_id':self.request.user.id})
      serializer.is_valid(raise_exception=True)
      order=serializer.save()
      serializer=OrderSerializers(order)
      return response.Response(serializer.data)
   
   def get_serializer_class(self):
      if self.request.method == 'POST':
         return CreateOrderSerializer
      elif self.request.method =='PATCH':
         return UpdateOrderSerializer
      return OrderSerializers
      

   def get_queryset(self):
      user = self.request.user

      if user.is_staff:
         return Order.objects.all()
      
      customer_id=Customer.objects.only('id').get(user_id=user.id)
      Order.objects.filter(customer_id=customer_id)
