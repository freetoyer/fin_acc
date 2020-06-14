from django.contrib import admin

from .models import Cheque, Entry, Shop, Product


admin.site.register(Cheque)
admin.site.register(Entry)
admin.site.register(Shop)
admin.site.register(Product)