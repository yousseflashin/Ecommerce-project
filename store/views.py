from django.shortcuts import render,get_object_or_404
from rest_framework import response,decorators,status
from django.http import HttpResponse
from .models import Collection, Product
from .serializers import ProductSerializer,CollectionSerializer
# Create your views here.

@decorators.api_view()
def product_list(request):
  products= Product.objects.select_related('collection').all()
  serialize=ProductSerializer(products,many=True,context={'request': request})
  return response.Response(serialize.data)


@decorators.api_view()
def collection_detail(request,pk):
  collections=Collection.objects.get(id=pk)
  serialize=CollectionSerializer(collections)
  return response.Response(serialize.data)



@decorators.api_view()
def product(request,id):
  product=get_object_or_404(Product,pk=id)
  serialize=ProductSerializer(product,context={'request': request})
  return response.Response(serialize.data)
  '''try:
    product= Product.objects.get(pk=id)
    serialize=ProductSerializer(product)
    return response.Response(serialize.data)
  except Product.DoesNotExist:
    return response.Response(status=status.HTTP_404_NOT_FOUND)'''