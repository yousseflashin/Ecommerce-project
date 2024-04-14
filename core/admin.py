from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from tags.models import Tag ,TaggedItem
from store.models import Product
from store.admin import AdminProduct,ProductImageInline
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
  add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","email", "password1", "password2","first_name","last_name"),
            },
        ),
    )

class  TagInLine(GenericTabularInline):
  model = TaggedItem
  autocomplete_fields=['tag']
  extra=1


admin.site.unregister(Product)

@admin.register(Product)
class CustomProductAdmin(AdminProduct):
  inlines=[TagInLine,ProductImageInline]
