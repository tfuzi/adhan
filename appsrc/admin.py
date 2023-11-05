from django.contrib import admin
from .models import Data

# Register your models here.
admin.site.site_header = "Hijri Date Admin"
admin.site.site_title = "Hijri Date Admin Portal"

admin.site.register(Data)