from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from datetime import datetime


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/%Y/%m/')
    identity_card = models.TextField(max_length=25)
    address = models.TextField(max_length=255)
    date_of_birth = models.DateField(default=datetime.strptime('01/01/2000', '%d/%M/%Y'))
    phone = models.TextField(max_length=15)
    notes = models.TextField(max_length=255, null=True)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Shipper(BaseModel):
    shipper = models.OneToOneField(User, on_delete=models.RESTRICT, primary_key=True)
    starting_date = models.DateField(auto_now=True)
    salary = models.DecimalField(default=0, max_digits=10, decimal_places=0)


class Customer(BaseModel):
    customer = models.OneToOneField(User, on_delete=models.RESTRICT, primary_key=True)
    membership_level = models.TextField(choices=(('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold')))


class Rating(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    shipper = models.ForeignKey(Shipper, on_delete=models.RESTRICT)
    rate = models.IntegerField(default=5)
    comment = models.TextField(max_length=255, null=True)


class Product(BaseModel):
    name = models.TextField(max_length=255, null=False)
    product_type = models.TextField(max_length=255)
    image = models.ImageField(upload_to='products/%Y/%m/')
    description = RichTextField()


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    shipper = models.ForeignKey(Shipper, on_delete=models.RESTRICT)
    name = models.TextField(max_length=255, null=False)
    delivery_charges = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    delivery_address = models.TextField(max_length=255, null=False)
    state = models.TextField(max_length=255, choices=(('draft', 'Draft'), ('auction', 'Auction'), ('waiting', 'Waiting'), ('shipped', 'Shipped'), ('done', 'Done')))
    delivery_date = models.DateTimeField()
    description = models.TextField(max_length=255, null=True)


class OrderDetail(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)


class Auction(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    auction_price = models.DecimalField(default=0, max_digits=10, decimal_places=0)


class Coupon(BaseModel):
    name = models.CharField(max_length=25, unique=True)
    discount_value = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    expiration_date = models.DateTimeField(default=datetime.strptime('01/01/2024', '%d/%M/%Y'))
    usage_limit = models.IntegerField(default=0)
    usage_conditions = models.DecimalField(default=100000, max_digits=10, decimal_places=0)


class CustomerCoupon(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    usage_limit = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=datetime.now())
    end_date = models.DateTimeField(default=datetime.strptime('01/01/2024', '%d/%M/%Y'))

