from django.urls import path
from . import views
#URLConf
urlpatterns = [
  path('products_list/',views.product_list),
  path('product/<int:id>/',views.product),
  path('collection_detail/<int:pk>/',views.collection_detail,name='collection_detail'),
] 