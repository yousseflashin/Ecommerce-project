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

from .task import notify_customers
#@transaction.atomic()
@api_view()
def say_hello(request):

    
  
  notify_customers.delay('hello')
  return render(request,'hello.html')