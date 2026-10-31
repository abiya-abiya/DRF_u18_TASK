from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
# faqat yaratilganda
# har save() da
# jadval yaratilmaydi, faqat meros
phone_validator = RegexValidator(
    regex=r'^\+998\d{9}$',
    message='Telefon +998XXXXXXXXX ko\'rinishida bo\'lsin.',
)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13, blank=True, validators=[phone_validator])
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.username