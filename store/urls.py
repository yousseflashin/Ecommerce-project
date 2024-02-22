from django.urls import path
from . import views
#URLConf
urlpatterns = [
  path('products_list/',views.ProductList.as_view()),
  path('product/<int:pk>/',views.ProductDetails.as_view()),
  path('collection_detail/<int:pk>/',views.CollectionDetails.as_view(),name='collection_detail'),
  path('collection_products/<int:pk>/',views.collection_products,name='collection_products'),
  path('collections/',views.CollectionList.as_view(),name='collections'),
] 