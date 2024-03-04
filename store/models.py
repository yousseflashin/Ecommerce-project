from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib import admin
from uuid import uuid4
# Create your models here.

class Pormotion(models.Model):
  description = models.CharField(max_length=255)
  discount=models.FloatField()



class Collection(models.Model):
  title=models.CharField(max_length=255)
  featured_product = models.ForeignKey("Product" , on_delete=models.SET_NULL,null=True,related_name='+')

  def __str__(self) -> str:
    return self.title
 
  class Meta:
    ordering =['title']


class Product(models.Model):
  title = models.CharField(max_length=255)
  slug=models.SlugField()#to find our product easly by browser
  description=models.TextField(null=True,blank=True,)
  unit_price=models.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(1)] )
  inventory = models.IntegerField(validators=[MinValueValidator(1)])
  last_update = models.DateTimeField(auto_now=True)
  collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
  pormotion=models.ManyToManyField(Pormotion,blank=True)
  
  def __str__(self) -> str:
    return self.title
  
  class Meta:
    ordering=['title']


class Customer(models.Model):
  MEMBERSHIP_BRONZE='B'
  MEMBERSHIP_SILVER='S'
  MEMBERSHIP_GOLD='G'
  MEMBERSHIP_CHOICES=[
    (MEMBERSHIP_BRONZE,'Bronze'),
    (MEMBERSHIP_SILVER,'Silver'),
    (MEMBERSHIP_GOLD,'Gold'),
  ]
  
  phone = models.CharField(max_length=18)
  birth_date = models.DateField(null=True)
  membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE )
  
  user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

  def __str__(self) -> str:
    return f'{self.user.first_name} {self.user.last_name}'

  @admin.display(ordering='user__first_name')
  def first_name(self):
    return self.user.first_name
  
  @admin.display(ordering='user__last_name')
  def last_name(self):
    return self.user.last_name
  
  def email(self):
    return self.user.email
  
  class Meta:
    
    db_table='store_customer'
    ordering=['user__first_name','user__last_name']
    indexes = [
     # models.Index(fields=['last_name','first_name'])
    ]



class Address(models.Model):
  street= models.CharField(max_length=255)
  city=models.CharField(max_length=255)
  zip=models.SmallIntegerField(null=True)
  customer=models.ForeignKey(Customer,on_delete=models.CASCADE)


class Order(models.Model):
  PAYMENT_PENDING='P'
  PAYMENT_COMPLETE='C'
  PAYMENT_FAILED='F'
  PAYMENT_STATUS=[
         (PAYMENT_PENDING,'Pending'),
         (PAYMENT_COMPLETE,'Complete'),
         (PAYMENT_FAILED,'Failed') 
  ]
  placed_at=models.DateTimeField(auto_now_add=True)
  payment_status=models.CharField(max_length=1,choices=PAYMENT_STATUS,default=PAYMENT_PENDING)
  customer=models.ForeignKey(Customer,on_delete=models.PROTECT)

  def __str__(self) -> str :
    return str(self.placed_at)

  



class OrderItem(models.Model):
  order =models.ForeignKey(Order,on_delete=models.PROTECT)
  product =models.ForeignKey(Product,on_delete=models.PROTECT)
  quantity=models.PositiveSmallIntegerField()
  unit_price=models.DecimalField(max_digits=6,decimal_places=2)



class Cart(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid4)
  created_at=models.DateTimeField(auto_now_add=True)



class CartItem(models.Model):
  cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity=models.PositiveSmallIntegerField(
    validators=[MinValueValidator(1)]
  )
  
  class Meta:
    unique_together = [['cart','product']]



class Review(models.Model):
  product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
  name=models.CharField(max_length=255)
  description=models.TextField()
  date=models.DateField(auto_now_add=True)
