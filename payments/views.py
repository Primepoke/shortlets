from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Payment, UserWallet
from django.conf import settings
from django.urls import reverse

from booking.models import Booking
from property.models import ManagerProfile

# Create your views here.


def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Retrieve submitted email
    submitted_email = request.session.pop('submitted_email', None)
      
    # Extract renter's email from the booking
    renter_email = booking.renter.user.email

    # Extract amount from the booking
    amount = booking.total_price

    # Use the submitted email if it's different, otherwise, use the renter's email
    email_to_use = submitted_email if submitted_email != renter_email else renter_email

    pk = settings.PAYSTACK_PUBLIC_KEY

    # Create a Payment
    payment = Payment.objects.create(amount=amount, email=email_to_use, booking=booking)
    payment.save()
    print(payment.email)

    # Store payment ID in session for verification in confirm_booking view
    request.session['payment_id'] = payment.id

    context = {
        'booking': booking,
        'payment': payment,
        'amount': amount, 
        'email': email_to_use,
        'paystack_pub_key': pk, 
        'amount_value': payment.amount_value()
    }
    
    return render(request, 'payments/verify_payment.html', context)



def verify_payment(request, ref):
    payment_id = request.session.get('payment_id')
    if not payment_id:
        messages.error(request, "Payment verification failed. Payment ID not found.")
        return render(request, 'payment/verify_failed.html')

    payment = get_object_or_404(Payment, id=payment_id, ref=ref)
    verified = payment.verify_payment()

    if verified:
        # Payment verified, update booking status and user wallet
        booking = payment.booking
        booking.save_confirmed()
        booking.save()

        user = booking.property.property_manager.user
        manager = get_object_or_404(ManagerProfile, user=user)
        print(user, manager)
        user_wallet, created = UserWallet.objects.get_or_create(manager_profile=manager)
        user_wallet.balance += payment.amount
        user_wallet.save()

        messages.success(request, "Booking and payment successful!")
        return redirect(reverse('listing_details', args=[booking.property.id]))
    else:
        messages.error(request, "Payment verification failed. Please contact support.")
        return render(request, 'payment/verify_failed.html')