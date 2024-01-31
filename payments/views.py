from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required #, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Payment, UserWallet

from booking.models import Booking
from accounts.models import ManagerProfile

from .forms import WalletCreationForm, WalletEditForm

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
        user_wallet, created = UserWallet.objects.get_or_create(manager_profile=manager)
        user_wallet.balance += payment.amount
        user_wallet.save()
        
        booking_id = booking.id
        booking_url = reverse('renter_booking_details', args=[booking_id])
        message = f"Congratulations! Booking and payment successful! <a href='{booking_url}'>Click here to view booking details</a>"

        messages.success(request, mark_safe(message))
        return redirect(reverse('listing_details', args=[booking.property.id]))
    else:
        messages.error(request, "Payment verification failed. Please contact your bank or support.")
        return render(request, 'payment/verify_failed.html')


def is_manager(user):
    # Check if the user is both logged-in and a manager
    return user.is_authenticated and hasattr(user, 'manager') 

def create_wallet(request):
    user = request.user

    if not is_manager(user):
        messages.error(request, 'Only property managers can create a wallet.')
        return redirect('login_view')

    manager = get_object_or_404(ManagerProfile, user=user)

    if request.method == 'POST':
        form = WalletCreationForm(request.POST)

        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.manager_profile = manager
            wallet.save()

            return redirect('view_wallet')

    # create wallet
    # wallet, created = UserWallet.objects.get_or_create(manager_profile=manager)
    
    form = WalletCreationForm()

    return render(request, 'payments/create_wallet.html', {'form': form})


@login_required
def edit_wallet(request, wallet_id):
    wallet = get_object_or_404(UserWallet, id=wallet_id)

    if request.method == 'POST':
        form = WalletEditForm(request.POST)

        if form.is_valid():
            wallet.account_number = form.cleaned_data['account_number']
            wallet.bank_name = form.cleaned_data['bank_name']
            wallet.save()

            return redirect('view_wallet')
    
    form = WalletEditForm()

    return  render(request, 'payments/edit_wallet.html', {'form': form})


@login_required
def view_wallet(request, wallet_id):
    wallet = get_object_or_404(UserWallet, id=wallet_id)

    return render(request, 'payments/wallet.html', {'wallet': wallet})