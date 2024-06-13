from rest_framework import status
import pytest 
from model_bakery import baker
from store.models import Collection
@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/',collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:
  #@pytest.mark.skip
  def test_if_user_is_anonymous_returns_401 (self,create_collection):
    # AAA (Arrange ,Act,Assert)
    #Arrange
    #Act-the beahvior to test
      response=create_collection({'title':'a'})
    #Assert
      assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_admin_returns_403 (self,authenticate,create_collection):
    # AAA (Arrange ,Act,Assert)
    #Arrange
      authenticate()
    #Act-the beahvior to test
      response=create_collection({'title':'a'})
    #Assert
      assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_user_is_invaled_returns_400 (self,authenticate,create_collection):
    # AAA (Arrange ,Act,Assert)
    #Arrange
      authenticate(is_staff=True)
    #Act-the beahvior to test
      
      response=create_collection({'title':''})
    #Assert
      assert response.status_code == status.HTTP_400_BAD_REQUEST
      assert response.data['title'] is not None

  def test_if_user_is_valed_returns_201 (self,authenticate,create_collection):
    # AAA (Arrange ,Act,Assert)
    #Arrange
      authenticate(is_staff=True)
    #Act-the beahvior to test
      response=create_collection({'title':'a'})
    #Assert
      print(response.data['title'])
      assert response.status_code == status.HTTP_201_CREATED
      assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_doesnt_exists_return_404(self,api_client):
        #Arrange
        
        #Act
          response=api_client.get(f'/store/collections/{id}/')
        #Assert
          assert response.status_code == status.HTTP_404_NOT_FOUND
          
    def test_if_collection_exists_return_200(self,api_client):
        #Arrange
          collection=baker.make(Collection)
          print(collection.__dict__)
        #Act
          response=api_client.get(f'/store/collections/{collection.id}/')
        #Assert
          assert response.status_code == status.HTTP_200_OK
          assert response.data == {
              'id':collection.id,
              'title':collection.title,
              'featured_product':collection.featured_product,
              'products_count':0,
          }
          
          