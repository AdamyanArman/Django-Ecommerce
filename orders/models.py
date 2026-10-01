from django.db import models
from users.models import Customer
from products.models import Product

# Create your models here.
class Cart(models.Model):
    customer=models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')

    def __str__(self) -> str:
        return f'Զամբյուղ {self.customer}'


    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=1)

    def __str__(self) -> str:
        return f"{self.cart}  {self.product}  {self.quantity}"


    @property
    def total_price(self):
        return self.product.price*self.quantity