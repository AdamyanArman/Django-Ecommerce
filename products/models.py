from django.db import models
import uuid

from django.db.models.enums import Choices


# Create your models here.
class Product(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article=models.CharField(max_length=15, unique=False)
    image=models.ImageField(upload_to='products/', blank=True, null=True)
    price=models.FloatField(blank=True, null=True)
    is_available=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.id



class ProductTranslations(models.Model):
    LANGUGES=[
        {'hy', 'Armenian'},
        {'en', 'English'},
        {'ru', 'Russian'}
    ]
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    language=models.CharField(max_length=10, choices=LANGUGES, default='hy')
    name=models.CharField(max_length=100)
    description=models.TextField(null=True)

    def __str__(self):
        return f'{self.name} {self.description}'


