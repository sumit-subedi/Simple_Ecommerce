from django.db import models
from django.conf import settings

# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to = "Category_Image/")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20)
    without_discount_price = models.IntegerField(null=True)
    with_discount_price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    out_of_stock = models.BooleanField(default=False)
    thumbnail = models.ImageField(
        upload_to='thumbnail',
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name

    def create_thumbnail(self):
        if not self.thumbnail:
            return

        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (200, 150)

        DJANGO_TYPE = self.thumbnail.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(BytesIO(self.thumbnail.read()))

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.thumbnail.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_thumbnail()
        force_update = False

        # If the instance already has been saved, it has an id and we set 
        # force_update to True
        if self.id:
            force_update = True

        super(Product, self).save(force_update=force_update)

   

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'Product_Images/')

    
    

class ProductDetails(models.Model):
    product = models.ForeignKey(Product, related_name='details', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description

class SliderImage(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to = 'Slider_images/')

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart' ,on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.item)

    class Meta:
        unique_together = ('user', 'item',) 


    
