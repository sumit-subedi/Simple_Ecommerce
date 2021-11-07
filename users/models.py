from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to = "Category_Image/")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20)
    without_discount_price = models.IntegerField()
    with_discount_price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    out_of_stock = models.BooleanField(default=False)

    def __str__(self):
        return self.name

   

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'Product_Images/')

class ProductDescription(models.Model):
    product = models.ForeignKey(Product, related_name='description', on_delete=models.CASCADE)
    description = models.TextField()

class SliderImage(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to = 'Slider_images/')

    def __str__(self):
        return self.name
    
