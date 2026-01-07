from django.db import models
import datetime
import uuid


class StatusChoice(models.TextChoices):
    AWAITING='awaiting'
    CONFIRMED='confirmed'
    FAILED='failed'

course_choice = (
    ('Introduction to Software Engineering', 'Introduction to Software Engineering'),
    ('Frontend Web Development(REACT)', 'Frontend Web Development(REACT)'),
    ('Backend Web Development (Python)', 'Backend Web Development (Python)'),
    ('Backend Web Development (Node.js)', 'Backend Web Development (Node.js)'),
)


class Payment(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    full_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    course = models.CharField(max_length=100, choices=course_choice)
    amount = models.PositiveIntegerField()
    reference = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.AWAITING)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Payment for: {self.email} - {self.status}'