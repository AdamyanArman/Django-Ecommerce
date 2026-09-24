from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Add / override fields here
    phone = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
    )

    # Optional: if you want phone to be used for login instead of username
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]  # username still required when creating superuser

    class Meta:
        verbose_name = "Հաճախորդ"
        verbose_name_plural = "Հաճախորդներ"

    def __str__(self) -> str:
        return f"{self.phone} {self.first_name}".strip()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()