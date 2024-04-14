<<<<<<< HEAD

from django.core.exceptions import ValidationError

def validate_file_size(file):
  max_size_gb = 1

  if file.size > max_size_gb*1000000000:
=======

from django.core.exceptions import ValidationError

def validate_file_size(file):
  max_size_gb = 1

  if file.size > max_size_gb*1000000000:
>>>>>>> 2524bd8b11a92f91b01009e2bf6749044b5b7cf9
      raise ValidationError(f'FILES CANNOT BE LARGER THAN{max_size_gb}gb!')