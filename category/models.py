from django.db import models

# Create your models here.
class Category(models.Model):
    products=models.ManyToManyField('products.Product', blank=True, related_name='categories')
    name_hy=models.CharField(max_length=255, null=False)
    name_en = models.CharField(max_length=255, null=False)
    name_ru = models.CharField(max_length=255, null=False)

    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)



    def __str__(self):
        all_products=', '.join([p.article for p in self.products.all()])
        return f'{self.name_hy} ({all_products})'