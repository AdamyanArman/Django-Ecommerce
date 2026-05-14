from django.db import models
import uuid

from django.db.models.enums import Choices


# Create your models here.
class Product(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article=models.CharField(max_length=15, unique=False)


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
    description=models.TextField()

    def __str__(self):
        return f'{self.name} {self.description}'


