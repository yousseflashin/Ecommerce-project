from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from . import views
#URLConf
route=DefaultRouter()
route.register('products',views.ProductViewSet,basename='products')
route.register('collections',views.CollectionViewSet)
route.register('carts',views.CartViewSet)
product_router = routers.NestedDefaultRouter(route,'products',lookup='product') 
product_router.register('reviews',views.ReviewViewSet,basename='product-reviews')
urlpatterns = [
  path('',include(route.urls)),
  path('',include(product_router.urls)),
  #path('collection_products/<int:pk>/',views.collection_products,name='collection_products'),

] 