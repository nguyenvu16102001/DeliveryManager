# Generated by Django 3.2.18 on 2023-03-25 12:03

import ckeditor.fields
import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(upload_to='users/%Y/%m/')),
                ('identity_card', models.TextField(max_length=25)),
                ('address', models.TextField(max_length=255)),
                ('date_of_birth', models.DateField(default=datetime.datetime(2000, 1, 1, 0, 1))),
                ('phone', models.TextField(max_length=15)),
                ('notes', models.TextField(max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=25, unique=True)),
                ('discount_value', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('expiration_date', models.DateTimeField(default=datetime.datetime(2024, 1, 1, 0, 1))),
                ('usage_limit', models.IntegerField(default=0)),
                ('usage_conditions', models.DecimalField(decimal_places=0, default=100000, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.TextField(max_length=255)),
                ('delivery_charges', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('delivery_address', models.TextField(max_length=255)),
                ('state', models.TextField(choices=[('draft', 'Draft'), ('auction', 'Auction'), ('waiting', 'Waiting'), ('shipped', 'Shipped'), ('done', 'Done')], max_length=255)),
                ('delivery_date', models.DateTimeField()),
                ('description', models.TextField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.TextField(max_length=255)),
                ('product_type', models.TextField(max_length=255)),
                ('image', models.ImageField(upload_to='products/%Y/%m/')),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, primary_key=True, serialize=False, to='delivery.user')),
                ('membership_level', models.TextField(choices=[('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shipper',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('shipper', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, primary_key=True, serialize=False, to='delivery.user')),
                ('starting_date', models.DateField(auto_now=True)),
                ('salary', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('number', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('rate', models.IntegerField(default=5)),
                ('comment', models.TextField(max_length=255)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='delivery.customer')),
                ('shipper', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='delivery.shipper')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='delivery.customer'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='delivery.shipper'),
        ),
        migrations.CreateModel(
            name='CustomerCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('usage_limit', models.IntegerField(default=0)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.coupon')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('auction_price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.order')),
                ('shipper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.shipper')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
