from django.contrib import admin

from .models import Docket, Document

# Register your models here.
admin.site.register((Docket, Document))