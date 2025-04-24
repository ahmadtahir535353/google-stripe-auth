from django.db import models
from orm.managers import UserManager, TransactionManager

from django.utils.timezone import now

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    phoneNumber = models.CharField(max_length=15, blank=True, null=True)

    password = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    email_verified = models.BooleanField(default=True)
    is_subscribed = models.BooleanField(default=False)

    remember_token = models.CharField(max_length=100, blank=True, null=True)
    remember_token_created_at = models.DateTimeField(blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email




class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=200, unique=True, null=True, blank=True)  # Optional, nullable
    session_id = models.CharField(max_length=200, unique=True, null=True, blank=True)  # Keep this non-unique unless needed
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='transactions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=now)

    # Custom manager
    objects = TransactionManager()

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"