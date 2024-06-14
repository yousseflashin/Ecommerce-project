from locust import HttpUser,task,between
from random import randint
import logging
class WebsiteUser(HttpUser):
  # Viewing poducts
   wait_time = between(1,5)

   @task(2)
   def view_products(self):
     collection_id=randint(3,7)
     self.client.get(
     f'/store/products/?collection_id={collection_id}',
     name='/store/products')

  # Viewing product details
   @task(4)
   def view_product(self):
     product_id = randint(1,1000)
     self.client.get(f'/store/products/{product_id}/',name='/store/products/:id')

  # Add product to cart
   @task(1)
   def add_to_cart(self):
     product_id = randint(1,10)
     self.client.post(
       f'/store/carts/{self.cart_id}/items/',
      name='/store/carts/items',
      json={'product_id':product_id,'quantity':1}
      )
    
   @task
   def say_hello(self):
       self.client.get('/playground/hello/',name='/playground/hello/')


   def on_start(self):
     response=self.client.post('/store/carts/')
     if response.status_code == 201:
            try:
                result = response.json()
                self.cart_id = result.get('id')
                if self.cart_id is None:
                    logging.error("Cart ID not found in the response: %s", response.text)
            except ValueError:
                logging.error("Failed to decode JSON response: %s", response.text)
                self.cart_id = None
     else:
            logging.error("Request failed with status code %d: %s", response.status_code, response.text)
            self.cart_id = None