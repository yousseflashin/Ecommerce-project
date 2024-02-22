from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from rest_framework import response,decorators,status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Collection, Product
from .serializers import ProductSerializer,CollectionSerializer
# Create your views here.



class ProductList(ListCreateAPIView):
  
    queryset= Product.objects.select_related('collection').all()

    serializer_class=ProductSerializer

    def get_serializer_context(self):
      return {'request': self.request}
     




class ProductDetails(RetrieveUpdateDestroyAPIView):
   
   queryset=Product.objects.all()
   serializer_class=ProductSerializer
   def get_serializer_context(self):
      return {'request': self.request}
   
   def delete(self,request,pk):
     product=get_object_or_404(Product,pk=pk)
     if product.orderitem_set.count() > 0:   
       product.delete()
       return response.Response({'error':'product cannot be deleted because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
     


class CollectionList(ListCreateAPIView):

  queryset=Collection.objects.annotate(products_count=Count('product')).select_related('featured_product').all()
  serializer_class=CollectionSerializer
  def get_serializer_context(self):
      return {'request': self.request}
  

class CollectionDetails(RetrieveUpdateDestroyAPIView):
  queryset=Collection.objects.annotate(products_count=Count('product')).all()
  serializer_class=CollectionSerializer

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





