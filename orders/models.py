from django.db import models
from users.models import Customer
from products.models import Product
from decimal import Decimal

# Create your models here.
class Cart(models.Model):
    customer=models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')

    def __str__(self) -> str:
        return f'Զամբյուղ {self.customer}'


    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def items_count(self):
        return self.items.filter(product__isnull=False).count()


class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    def __str__(self) -> str:
        return f"{self.cart}  {self.product}  {self.quantity}"


    @property
    def subtotal(self):
        return self.product.price*self.quantity


class Order(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        POS = "pos", "POS terminal"
        IDRAM = "idram", "Idram"
        AMERIA_ONLINE = "ameria_online", "Ameria Bank online"

    class Status(models.TextChoices):
        NEW = "new", "New"
        ACCEPTED = "accepted", "Accepted"
        COLLECTING_BEGIN = "collecting_begin", "Collecting begin"
        COLLECTED = "collected", "Collected"
        ON_ROAD = "on_road", "On road"
        ORDERED = "ordered", "Ordered"
        CANCELLED = "cancelled", "Cancelled"

    # Կապ հաճախորդի հետ (եթե պատվերը կապված է օգտատիրոջ հետ)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders', null=True, blank=True)

    # Անձնական և առաքման տվյալներ
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    comment = models.TextField(blank=True)

    # Վճարում և կարգավիճակ
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
    )
    is_paid = models.BooleanField(default=False)

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.NEW,
    )

    # Ամսաթվեր
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.name} {self.surname}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def items_count(self):
        return self.items.count()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.price is None and self.product:
            self.price = self.product.price

        if self.quantity is None:
            self.quantity = Decimal('1.000')

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        # Օգտագործում ենք str(self.product)՝ անկախ նրանից, թե Product մոդելն ինչ դաշտեր ունի
        product_name = str(self.product) if self.product else "Ջնջված ապրանք"
        return f"{product_name} x {self.quantity} (Պատվեր #{self.order.id})"

    @property
    def subtotal(self):
        if self.price is None or self.quantity is None:
            return Decimal('0.00')
        return self.price * self.quantity