from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from . import views
#URLConf
route=DefaultRouter()
route.register('products',views.ProductViewSet)
route.register('collections',views.CollectionViewSet)
urlpatterns = [
  path('',include(route.urls)),
  #path('collection_products/<int:pk>/',views.collection_products,name='collection_products'),

] 