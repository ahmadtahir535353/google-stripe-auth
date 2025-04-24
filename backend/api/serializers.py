from rest_framework import serializers

from orm.models import User  , Transaction
from django.contrib.auth.hashers import make_password
import logging
logger = logging.getLogger(__name__)

      
class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'password', 
            'is_active','is_subscribed', 'date_joined', 'country', 'city', 'zip', 'phoneNumber','profile_picture'
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
            'country': {'required': False, 'allow_null': True},
            'city': {'required': False, 'allow_null': True},
            'zip': {'required': False, 'allow_null': True},
            'phoneNumber': {'required': False, 'allow_null': True},
            'profile_picture': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        # Check if 'set_password_later' flag is in validated_data
        set_password_later = validated_data.pop('set_password_later', False)
        
        if not set_password_later and 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        
        user = super().create(validated_data)

        # Optionally set password to None or handle as needed if the flag was true
        if set_password_later:
            user.password = None  # or handle this according to your logic

        user.save()  # Save the user after creation
        return user
    
    def update(self, user, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(user, validated_data)
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'amount', 'transaction_id', 'user', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']  # Fields that should not be modified

    def validate_amount(self, value):
        """
        Ensure the transaction amount is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("The amount must be greater than zero.")
        return value

    def validate_status(self, value):
        """
        Ensure the status is one of the valid choices.
        """
        valid_statuses = [choice[0] for choice in Transaction.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Valid options are: {valid_statuses}")
        return value

    def create(self, validated_data):
        """
        Custom create logic for transactions.
        """
        transaction = super().create(validated_data)
        # Additional custom logic (e.g., logging, notifications) can go here
        return transaction

class AuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    #ignore this
    error = serializers.CharField(required=False)