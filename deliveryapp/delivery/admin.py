from django.contrib import admin
from .models import Shipper, Customer, Order, User, Product
from django.utils.html import mark_safe
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'shipper', 'name', 'delivery_charges', 'delivery_address', 'state',
                    'delivery_date', 'description']
    search_fields = ['customer', 'shipper', 'name', 'state']
    list_filter = ['customer', 'shipper', 'name', 'state']


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['image']

    def image(self, user):
        return mark_safe("<img src='/static/{img_url}' width='120'/>".format(img_url=user.avatar.name))


admin.site.register(User, UserAdmin)
admin.site.register(Shipper)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product)
