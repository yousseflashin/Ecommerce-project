from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.aggregates import Min,Max,Avg,Sum 
from django.db.models import Q,F,Value,Func,Count,ExpressionWrapper,DecimalField
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Concat
from django.db import transaction
from django.db import connection

from django.core.mail import send_mail,mail_admins,BadHeaderError,EmailMessage

from templated_mail.mail import BaseEmailMessage 

from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Product,OrderItem,Customer,Order,Collection,Pormotion
from tags.models import TaggedItem

#@transaction.atomic()
@api_view()
def say_hello(request):
 try:
    #send_mail('subject','message','info@store.com',['youssef.mlashin@gmail.com'])
    #mail_admins('subject','message',html_message='message')
    #message=EmailMessage('subject','message','from@store.com',['youssef.mlashin@gmail.com'])
    #message.attach_file('playground/static/images/Capture.PNG')
    #message.send()
    message = BaseEmailMessage(
      template_name='emails/hello.html',
      context={'name':'youssef'}
    )
    message.send(['youssef.mlashin@gmail.com'])
 except BadHeaderError:
   pass
 

 #query_set = Product.objects.filter(unit_price__range=(10,60))
 #query_set = Product.objects.filter(unit_price__gt=50)
 #query_set = Product.objects.filter(unit_price__lt=50)
 #query_set = Product.objects.filter(unit_price__lte=50)
 #query_set = Product.objects.filter(unit_price__gte=50)
 #query_set = Product.objects.filter(title__contains="Coffee")
 #query_set = Product.objects.filter(title__icontains="coffee")
 #query_set = Product.objects.filter(unit_price__in=[1,2,3])
 #query_set = Product.objects.filter(last_update__year=2016)
 #query_set = Product.objects.filter(inventory__lt=10,unit_price__lt=20)
 #query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

 #query_set = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__lt=20))
 #query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

 #query_set = Product.objects.filter(inventory=F("collection") )

 #query_set =Product.objects.order_by('unit_price')
 #query_set =Product.objects.order_by('-unit_price')
 #query_set =Product.objects.order_by('unit_price').reverse()
 #query_set =Product.objects.order_by('unit_price','inventory')
 #query_set =Product.objects.order_by('unit_price','inventory').reverse()
 #query_set =Product.objects.order_by('unit_price').reverse()

 #product =Product.objects.order_by('unit_price')[0]
 #product =Product.objects.earliest('unit_price')
 #product =Product.objects.latest('unit_price')

 #query_set=Product.objects.all()[:10]
 #query_set=Product.objects.all()[5:10]

 #query_set=Product.objects.values_list('id','title','collection__title') 
 #query_set=Product.objects.values('id','title','collection__title') 
 #query_set=OrderItem.objects.values_list('product__title').order_by('product__title').distinct()
 #query_set=Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

 #query_set=Product.objects.only('pk','title')
 #query_set=Product.objects.defer('title')

 

 #query_set=Customer.objects.prefetch_related('order_set')
 #query_set=Customer.objects.prefetch_related('pormotion')
 #query_set=Order.objects.select_related('customer').order_by('customer__first_name')

 #totalNumberOfCustomer=Customer.objects.aggregate(Count('id'))
 #totalPrice=Product.objects.aggregate(total=Sum('unit_price'))
 #minPrice=Product.objects.aggregate(total=Min('unit_price'))
 #maxPrice=Product.objects.aggregate(total=Max('unit_price'))
 #query_set=Customer.objects.annotate(is_new=Value(True))
 #query_set=Customer.objects.annotate(new_id=F('id'))
 #query_set=Customer.objects.annotate(new_id=F('id')+1)

 #query_set=Customer.objects.annotate(new_field=Func(F('first_name'),Value(' '),F('last_name') ,function='CONCAT'))
 #query_set=Customer.objects.annotate(new_field=Concat('first_name',Value(' '),'last_name'))
 #query_set=Customer.objects.annotate(number_of_orders=Count('order'))

 #discountprice=ExpressionWrapper(F('unit_price')*0.8,output_field=DecimalField())
 #query_set=Product.objects.annotate(discount_price=discountprice)

 #query_set= TaggedItem.objects.get_tags_for(Product,1)

 #query_set = Product.objects.all()
 #list(query_set)
 #query_set[0]
 
 #collection=Collection()
 #collection.title='Video Games'
 #collection.featured_product=Product(pk=1)
 #collection.save()
 #collection=Collection(title='a',featured_product_id=1)
 #Collection.objects.create(title='a',featured_product_id=1)

 #collection=Collection(pk=11)
 #collection.featured_product=None
 #collection.save()

 #collection=Collection.objects.get(pk=11)
 #collection.featured_product=None
 #collection.save()

 #collection=Collection.objects.filter(pk=11).create(featured_product=None)

 #collection=Collection.objects.get(pk=11)
 #collection.delete()
 #Collection.objects.filter(id__gt=5).delete()

 '''#with transaction.atomic():
   # order=Order()
   # order.customer_id = 1
   # order.save()

    #item=OrderItem()
    #item.order=order
    #item.product_id=1
    #item.quantity=1
    #item.unit_price=10
    #item.save()'''
    
 #query_set= Product.objects.raw('select * from store_product')

 #with connection.cursor() as cursor:
  # cursor.callproc('get_customers',[1,2,'a'])

 #context={
     #'product':product
     #'orders':list(query_set)
     #'totalNumberOfCustomer':totalNumberOfCustomer,
     #'totalPrice':totalPrice,
     #'minPrice':minPrice,
     #'maxPrice':maxPrice,
  
 #}
 return render(request,'hello.html')