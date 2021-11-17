# Generated by Django 3.2.9 on 2021-11-16 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20211115_1543'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('created',)},
        ),
        migrations.AlterModelOptions(
            name='orderdetail',
            options={'ordering': ('created',)},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('created',)},
        ),
        migrations.AlterModelOptions(
            name='shippingaddress',
            options={'ordering': ('created',)},
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
