from rest_framework import status
import pytest 
from model_bakery import baker
from store.models import Product,Collection
from decimal import *
@pytest.fixture
def create_product(api_client):
  def do_create_product(product):
     return api_client.post('/store/products/',product)
  return do_create_product

@pytest.mark.django_db
class TestCreateProduct:
  def test_if_user_is_anonymous_returns_401 (self,create_product):
    #Arrange
    #Act
     response=create_product({'title':'a'})
    #assert
     assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_admin_returns_403 (self,authenticate,create_product):
    #Arrange
     authenticate()
    #Act
     response=create_product({'title':'a'})
    #assert
     assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_user_is_invalde_returns_400 (self,authenticate,create_product):
    #Arrange
     authenticate(is_staff=True)
    #Act
     response=create_product({'title':''})
    #assert
     assert response.status_code == status.HTTP_400_BAD_REQUEST
     assert response.data['title'] is not None
  
  def test_if_user_is_valed_returns_201 (self,authenticate,create_product):
    #Arrange
     authenticate(is_staff=True)
     collection = Collection.objects.create(title="Test Collection")
    #Act
     response=create_product({'title':'a','slug':'-','inventory':1,'unit_price':Decimal('1'),'collection':collection.id})
    #assert
     print(response.data)
     assert response.status_code == status.HTTP_201_CREATED
     assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveProduct:
  def test_if_product_doesnt_exist_404(self,api_client):
     #arrange
       
      #Act
       response=api_client.get(f'/store/products/{id}/')
      #assert
       assert response.status_code == status.HTTP_404_NOT_FOUND 

  def test_if_product_exist_200(self,api_client):
     #arrange
       
       product=baker.make(Product)
       
       print(product.__dict__)
      #Act
       response=api_client.get(f'/store/products/{product.id}/')
      #assert
       assert response.status_code == status.HTTP_200_OK



   