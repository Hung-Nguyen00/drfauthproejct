from io import BytesIO
from django.db import models
from django.template.defaultfilters import slugify
from PIL import Image
import uuid
from model_utils.models import TimeStampedModel
from django.core.files import File
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
# Create your models here.


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Product(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    price = models.DecimalField(default=0, max_digits=11, decimal_places=2)
    image = models.ImageField(upload_to='uploads/',null=True, blank=True)
    thumbnail = models.ImageField(upload_to='',null=True, blank=True)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.code

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            domain = Site.objects.get_current().domain
            return f'https://{domain}' + self.image.url
        return ''
    
    def get_thumbnail(self):
        domain = Site.objects.get_current().domain
        if self.thumbnail:
            return f'https://{domain}' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return f'https://{domain}' + self.thumbnail.url
            else:
                return ''
            
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image).convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=50)
        
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail     
        
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if Product.objects.filter(slug=slug):
            self.slug = slug + '-' + self.code
        else:
            self.slug = slug
        super(Product, self).save(*args, **kwargs)


class Order(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    complete = models.BooleanField(default=False)
    total = models.DecimalField(default=0, max_digits=11, decimal_places=2)

    class Meta:
        ordering = ('created',)



class OrderDetail(TimeStampedModel):
    product = models.ForeignKey(
        Product, related_name="order_product", on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, related_name="order_detail",
                              on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=11, decimal_places=2)

    class Meta:
        ordering = ('created',)

    @property
    def get_total(self):
        return self.quantity * self.price


class ShippingAddress(TimeStampedModel):
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL, related_name="shiping_user")
    order = models.ForeignKey(Order, blank=True, null=True,
                              on_delete=models.SET_NULL, related_name="shiping_order")
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return str(self.address)
