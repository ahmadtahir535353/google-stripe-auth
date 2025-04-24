import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from orm.models import Transaction
from ..decorators import token_auth_required

# Set your Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
    @token_auth_required
    def post(self, request, *args, **kwargs):
        try:
            user = request.user

            # Check if the user is already subscribed
            if user.is_subscribed:
                return JsonResponse({
                    'status': False,
                    'message': "Already subscribed"
                }, status=400)

            # Check if there's an existing pending transaction for the user
            pending_transaction = Transaction.objects.filter(
                user=user, status='pending'
            ).first()

            # Create or update the Stripe Checkout session
            if pending_transaction:
                # Update existing transaction session with a new Stripe Checkout session
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {'name': 'Test Service'},
                                'unit_amount': 20 * 100,  # Amount in cents
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url=f'{settings.FRONTEND_URL}/home?type=success',
                    cancel_url=f'{settings.FRONTEND_URL}/home?type=cancel',
                )
                pending_transaction.session_id = checkout_session.id
                pending_transaction.save()
            else:
                # Create a new transaction and Stripe Checkout session
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {'name': 'Test Service'},
                                'unit_amount': 20 * 100,  # Amount in cents
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url=f'{settings.FRONTEND_URL}/home?type=success',
                    cancel_url=f'{settings.FRONTEND_URL}/home?type=cancel',
                )
                Transaction.objects.create(
                    session_id=checkout_session.id,
                    user=user,
                    amount=20,  # Convert cents to dollars
                    status='pending',
                )

            # Return the session URL to the frontend
            return JsonResponse({
                'stripe_url': checkout_session.url
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    