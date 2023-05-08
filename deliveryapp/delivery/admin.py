from django.db.models.functions import Extract

from django.contrib import admin
from django.template.response import TemplateResponse
from .models import Shipper, Customer, Order, User, Product, OrderDetail, Coupon, CustomerCoupon
from django.utils.html import mark_safe
from django.urls import path
from django.db.models import Sum, Count
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'shipper', 'name', 'delivery_charges', 'delivery_address', 'state',
                    'delivery_date', 'description', 'created_date']
    search_fields = ['customer', 'shipper', 'name', 'state', 'delivery_date', 'created_date']
    list_filter = ['customer', 'shipper', 'name', 'state', 'delivery_date', 'created_date']


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['image']

    def image(self, user):
        return mark_safe("<img src='/static/{img_url}' width='120'/>".format(img_url=user.avatar.name))


class DeliveryAppAdminSite(admin.AdminSite):
    site_header = 'HE THONG QUAN LY GIAO HANG'

    def get_urls(self):
        return [
            path('delivery-stats/', self.delivery_stats)
        ] + super().get_urls()

    def delivery_stats(self, request):
        year = request.GET.get('year')
        delivery_stats = ''
        if year:
            delivery_stats = Order.objects.values('delivery_date__month')\
                                        .annotate(total=Sum('delivery_charges'), count=Count('id'))\
                                        .filter(active=True, delivery_date__year=year, state='done')\
                                        .order_by('delivery_date__month')

        return TemplateResponse(request, 'admin/delivery-stats.html', {
            'year': year,
            'delivery_stats': delivery_stats
        })


admin_site = DeliveryAppAdminSite('deliverymanager')


admin_site.register(User, UserAdmin)
admin_site.register(Shipper)
admin_site.register(Customer)
admin_site.register(Order, OrderAdmin)
admin_site.register(Product)
admin_site.register(Coupon)
admin_site.register(CustomerCoupon)

