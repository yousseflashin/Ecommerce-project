from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from tags.models import Tag ,TaggedItem
from store.models import Product
from store.admin import AdminProduct
# Register your models here.
class  TagInLine(GenericTabularInline):
  model = TaggedItem
  autocomplete_fields=['tag']
  extra=1


admin.site.unregister(Product)

@admin.register(Product)
class CustomProductAdmin(AdminProduct):
  inlines=[TagInLine]
