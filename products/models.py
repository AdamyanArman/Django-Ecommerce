import uuid
from django.db import models


class Attribute(models.Model):
    name_hy = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)

    def __str__(self):
        return self.name_hy


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="values"
    )
    value_hy = models.CharField(max_length=50)
    value_en = models.CharField(max_length=50)
    value_ru = models.CharField(max_length=50)

    def __str__(self):
        # Fallback to prevent crashes if attribute isn't loaded yet
        attr_name = self.attribute.name_hy if hasattr(self, 'attribute') else ''
        return f"{attr_name}: {self.value_hy}"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.CharField(max_length=15)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    # FIXED: Replaced FloatField with DecimalField for financial accuracy
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    is_available = models.BooleanField(default=False)

    attribute_values = models.ManyToManyField(
        AttributeValue,
        through="ProductAttributeValue",
        related_name="products",
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # FIXED: Safe retrieval without crashing on missing translations
        translation = self.translations.filter(language="hy").first()
        return translation.name if translation else f"Product {self.article}"


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("product", "attribute_value")


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