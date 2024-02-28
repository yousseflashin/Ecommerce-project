from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import response,decorators,status
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,RetrieveModelMixin
from .filters import ProductFilter
from .models import Cart, Collection, Product,OrderItem,Review,CartItem
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSeralizer,AddCartItemSerializer,CartItemSeralizer
from .pagination import DefaultPagination
# Create your views here.


class ProductViewSet(ModelViewSet):
    
    queryset= Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
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
   
   def get_serializer_class(self):
      if self.request.method == 'POST':
         return AddCartItemSerializer
      return CartItemSeralizer
    

   def get_serializer_context(self):
       return {'cart_id':self.kwargs['cart_pk']}
   

   def get_queryset(self):
      return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
