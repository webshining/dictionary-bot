from django.contrib import admin

from .models import Dictionary, Word

# Register your models here.
admin.site.register(Dictionary)
admin.site.register(Word)
