import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from orm.models import Transaction, User

stripe.api_key = settings.STRIPE_SECRET_KEY

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            # Verify webhook signature
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )

            # Handle successful payment
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']  # Get session object
                session_id = session.get('id')

                # Find the session in the database and update its status to 'successful'
                checkout_session = Transaction.objects.get(session_id=session_id)
                checkout_session.status = 'successful'
                checkout_session.save()

                # If the payment is successful, update the user's subscription status
                user = checkout_session.user
                user.is_subscribed = True
                user.save()

            # Handle payment failure
            elif event['type'] == 'checkout.session.async_payment_failed':
                session = event['data']['object']
                session_id = session.get('id')

                # Find the session in the database and update its status to 'failed'
                checkout_session = Transaction.objects.get(session_id=session_id)
                checkout_session.status = 'failed'
                checkout_session.save()

            # Respond with a success status to Stripe
            return JsonResponse({'status': 'success'})

        except ValueError as e:
            # Invalid payload
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return JsonResponse({'error': 'Invalid signature'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
