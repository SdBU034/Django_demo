from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, validators=[MinLengthValidator(4)])
    password = models.CharField(max_length=16, validators=[MinLengthValidator(6)])
    telephone = models.CharField(max_length=11, validators=[RegexValidator(r'1[3455678]\d{9}')])

    class Meta:
        db_table = 'user'
