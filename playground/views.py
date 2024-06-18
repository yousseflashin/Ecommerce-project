from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.aggregates import Min,Max,Avg,Sum 
from django.db.models import Q,F,Value,Func,Count,ExpressionWrapper,DecimalField
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Concat
from django.db import transaction
from django.db import connection
from django.views.decorators.cache import cache_page
from django.core.mail import send_mail,mail_admins,BadHeaderError,EmailMessage
from django.utils.decorators import method_decorator

from templated_mail.mail import BaseEmailMessage 

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Product,OrderItem,Customer,Order,Collection,Pormotion
from tags.models import TaggedItem
import requests
from .task import notify_customers
#@transaction.atomic()
#@api_view()
class HelloView(APIView):
    @method_decorator(cache_page(5*60))
    def get(self,request):
         response=requests.get('https://httpbin.org/delay/2')
         data = response.json()
         return render(request,'hello.html')

        

    
  #notify_customers.delay('hello')
  #return render(request,'hello.html')