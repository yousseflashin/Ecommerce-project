from typing import Any
from django.contrib import admin,messages
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.http.request import HttpRequest
from django.http import HttpResponse
from django.utils.html import format_html,urlencode
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline
from tags.models import Tag ,TaggedItem
from . import models

class InventoryFilter(admin.SimpleListFilter):
   
   title='inventory'
   parameter_name='inventory'
   
   def lookups(self, request, model_admin):
     return [
       ('<10','Low')
     ]
   
   def queryset(self, request ,queryset:QuerySet) :
     if self.value()=='<10':
        return queryset.filter(inventory__lt=10)
     

# Register your models here.
@admin.register(models.Product)
class AdminProduct(admin.ModelAdmin):
  
  search_fields=['title']
  autocomplete_fields=['collection']
  prepopulated_fields={
    'slug':['title']
  }
  actions=['clear_inventory']
  list_display=['title', 'unit_price', 'inventory_status' ,'last_update' ,'collection', 'slug']
  list_editable=['unit_price']
  list_select_related=['collection']
  list_filter=['collection','last_update',InventoryFilter,'collection__id']
  ordering=['title','unit_price']
  list_per_page=20
 
  @admin.action(description = 'clear_inventory')
  def clear_inventory(self,request,queryset:QuerySet):
    update_count=queryset.update(inventory=0)
    self.message_user(
        request,
        f'{update_count} products inventory were succesfully removed',
        messages.ERROR,
       
    )

  @admin.display(ordering='inventory')
  def inventory_status(self,product):
    if product.inventory<10:
      return 'Low'
    return 'Ok'


@admin.register(models.Customer)
class AdminCustomer(admin.ModelAdmin):
  list_display=['first_name' ,'last_name','email','phone','birth_date','membership','order_count']
  list_editable=['membership']
  list_per_page=20
  ordering=['user__first_name','user__last_name']
  search_fields=['first_name__istartswith','last_name__istartswith']
  autocomplete_fields=['user']
  @admin.display(ordering='order_count')
  def order_count(self,customer):
    url=(reverse('admin:store_order_changelist') + '?' +  urlencode({'customer__id':str(customer.id)})) 
    return format_html('<a href="{}">{}</a>',url,customer.order_count)
  
  def get_queryset(self, request):
      return super().get_queryset(request).annotate(order_count=Count('order'))
  

@admin.register(models.Collection)
class AdminCollection(admin.ModelAdmin):

  search_fields=['title']
  autocomplete_fields=['featured_product']
  list_display=['title','products_count']

  @admin.display(ordering='product_count')
  def products_count(self,collection):
    url=(reverse('admin:store_product_changelist') + '?' +  urlencode({'collection__id':str(collection.id)})) 
    return format_html('<a href="{}">{}</a>',url,collection.products_count)


  def get_queryset(self, request):
    return super().get_queryset(request).annotate(products_count=Count('product'))


@admin.register(models.Cart)
class AdminCart(admin.ModelAdmin):

  list_display=[]


class OrderItemLine(admin.TabularInline):

  model=models.OrderItem
  autocomplete_fields=['product']
  extra=1


@admin.register(models.Order)
class AdminOrder(admin.ModelAdmin):

  autocomplete_fields=['customer']
  inlines=[OrderItemLine]
  list_display=['customer','payment_status','placed_at']
  list_select_related=['customer']
  list_filter=['customer__id']

  def customer_order(self,order):
    return order.customer.first_name
    


