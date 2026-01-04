from django.db import models
import datetime
import uuid


class StatusChoice(models.TextChoices):
    AWAITING='awaiting'
    CONFIRMED='confirmed'
    FAILED='failed'

class Payment(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    full_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    course = models.CharField(max_length=100, blank=False, null=False)
    amount = models.PositiveIntegerField()
    reference = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.AWAITING)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.email} - {self.status}'