from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    name         = models.CharField(max_length=30)
    email        = models.CharField(max_length=100, unique=True)
    kakao_id     = models.CharField(max_length=50, unique=True)
    gender       = models.CharField(max_length=10, default='undefined')
    point        = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.name