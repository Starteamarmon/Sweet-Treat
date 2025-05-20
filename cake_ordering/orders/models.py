from django.db import models
from django.utils import timezone

class Order(models.Model):
    CAKE_CHOICES = [
        ('Red_cake', 'Красный бархат'),
        ('Honey', 'Медовик'),
        ('Apricot','Абрикосовый'),
        ('Vanilla','Ванильный'),
        ('Poppy','Маковый'),
    ]

    telegram_id = models.BigIntegerField()
    cake_name = models.CharField(max_length=255, choices=CAKE_CHOICES)
    weight = models.FloatField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.id}'