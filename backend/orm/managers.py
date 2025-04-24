from django.db import models
from django.utils import timezone




class UserManager(models.Manager):

    def get_user(self, id):
        return self.filter(id=id).first()

    def get_all_users(self):
        return self.all()

class TransactionManager(models.Manager):
    def get_transaction_by_id(self, transaction_id):
        """Fetch a single transaction by its ID."""
        return self.filter(id=transaction_id).first()

    def get_transactions_by_user(self, user_id):
        """Fetch all transactions for a specific user."""
        return self.filter(user_id=user_id).all()

    def get_recent_transactions(self, days=30):
        """Fetch transactions created in the last `days`."""
        from django.utils.timezone import now
        start_date = now() - timezone.timedelta(days=days)
        return self.filter(created_at__gte=start_date).all()

    def get_successful_transactions(self):
        """Fetch all transactions marked as successful."""
        return self.filter(status='successful').all()