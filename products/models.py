import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Brand(models.Model):
    name_hy = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name_hy}'


class Type(models.Model):
    value_hy = models.CharField(max_length=50)
    value_en = models.CharField(max_length=50)
    value_ru = models.CharField(max_length=50)


    def __str__(self):
        return f'{self.value_hy}'

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.CharField(max_length=15)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    # FIXED: Replaced FloatField with DecimalField for financial accuracy
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    is_available = models.BooleanField(default=False)

    first_step = models.DecimalField(
        "Առաջին քայլ", max_digits=6, decimal_places=2, default=Decimal("1.00"),
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Զամբյուղ ավելացնելիս սկզբնական քանակը (նաև նվազագույնը)",
    )
    next_step = models.DecimalField(
        "Հաջորդ քայլ", max_digits=6, decimal_places=2, default=Decimal("1.00"),
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="+ / − սեղմելիս փոփոխության քայլը",
    )
    max_quantity = models.DecimalField(
        "Առավելագույն քանակ", max_digits=8, decimal_places=1, default=Decimal("100.0"),
        validators=[MinValueValidator(Decimal("0.1"))],
        help_text="Զամբյուղում այս քանակից ավել չի կարելի ավելացնել",
    )

    brand=models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    type=models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # FIXED: Safe retrieval without crashing on missing translations
        translation = self.translations.filter(language="hy").first()
        return translation.name if translation else f"Product {self.article}"


class ProductTranslations(models.Model):
    LANGUAGES = [
        ("hy", "Armenian"),
        ("en", "English"),
        ("ru", "Russian"),
    ]
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="translations"
    )
    language = models.CharField(max_length=10, choices=LANGUAGES, default="hy")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("product", "language")

    def __str__(self):
        return f"{self.language.upper()}: {self.name}"