from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from rest_framework import response,decorators,status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Collection, Product,OrderItem,Review
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer
# Create your views here.


class ProductViewSet(ModelViewSet):
    
    serializer_class=ProductSerializer
    def get_queryset(self):
      queryset= Product.objects.all()
      collection_id = self.request.query_params.get('collection_id')
      if collection_id is not None:
         queryset=queryset.filter(collection_id=collection_id)
      return queryset
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


