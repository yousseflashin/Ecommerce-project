from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from . import views
#URLConf
route=DefaultRouter()
route.register('products',views.ProductViewSet,basename='product_route')
route.register('collections',views.CollectionViewSet,basename='collection_route')
route.register('carts',views.CartViewSet,basename='cart_route')
route.register('customers',views.CustomerViewSet)
route.register('order',views.OrderViewSet,basename='order')

product_router = routers.NestedDefaultRouter(route,'products',lookup='product') 
product_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

carts_router=routers.NestedDefaultRouter(route,'carts',lookup='cart')
carts_router.register('items',views.CartItemViewSet,basename='cart-item-list')

urlpatterns = [
  path('',include(route.urls)),
  path('',include(product_router.urls)),
  path('',include(carts_router.urls)),
  #path('collection_products/<int:pk>/',views.collection_products,name='collection_products'),

] 