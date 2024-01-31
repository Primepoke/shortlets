from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Booking
from .forms import BookingForm, LoginCheckForm, AvailabilityForm
from .utils import is_property_available
from datetime import date

from accounts.models import ManagerProfile, RenterProfile
from property.models import Property
from payments.forms import ConfirmBookingForm

# Create your views here.



def check_availability(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date'].date() 
            end_date = form.cleaned_data['end_date'].date() 

            if start_date> end_date:
                messages.warning(request, "Start date should be before end date.")
                return redirect(reverse('check_availability', args=[property_id]))

            status, message = is_property_available(property, start_date, end_date)

            if status:
                messages.success(request, message)
                return redirect(reverse('listing_details', args=[property_id]))
            else:
                messages.warning(request, message)
                return redirect(reverse('listing_details', args=[property_id]))
    else:
        form = AvailabilityForm()

    return render(request, 'booking/check_availability.html', {'property': property, 'form': form})



def login_check(request):
    if request.method == 'POST':
        user = request.user
        form = LoginCheckForm(request.POST)

        if form.is_valid():
            question = form.cleaned_data.get('question')  # Use cleaned_data to get form data

            if question == 'yes':
                # If user response is yes, try to log in the user and redirect accordingly     
                try:
                    login(request, user)
                except Exception as e:
                    messages.warning(request, f"We couldn't find a matching User Profile. Please Login if you have an account or register an account.")
                    target_view_url = reverse('register')
                    return redirect(target_view_url)

                # Check if the user has a renter profile
                if hasattr(user, 'renter'):
                    return redirect('create_booking')
                else:
                    messages.warning(request, "We couldn't find a matching Renter Profile. Please register as a Renter.")
                    target_view_url = reverse('renter_registration')
                    return redirect(target_view_url)
                
            elif question == 'no':
                messages.warning(request, "Please register an account before proceeding.")
                target_view_url = reverse('register')
                return redirect(target_view_url)
        
        # Handle the case where the form is not valid
        else:
            messages.warning(request, "Invalid form submission. Please try again.")

    # Render the initial form
    form = LoginCheckForm()
    return render(request, 'booking/login_check.html', {'form': form})


def create_booking(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    user = request.user

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['check_in_datetime'].date()
            end_date = form.cleaned_data['check_out_datetime'].date()

            # Call the availability check function
            status, message = is_property_available(property, start_date, end_date)

            if status:
                # Property is available, continue with booking process
                booking = form.save(commit=False)
                booking.property = property

                # Store form data in the session
                form_data = form.cleaned_data
                form_data['check_in_datetime'] = form_data['check_in_datetime'].isoformat()
                form_data['check_out_datetime'] = form_data['check_out_datetime'].isoformat()
                request.session['booking_form_data'] = form_data

                if user.is_authenticated:
                    # If the user is authenticated, check for a renter profile
                    if hasattr(user, 'renter'):
                        booking.renter = user.renter
                        booking.get_total_price()
                        booking.save_unconfirmed()
                        booking.save()

                        return redirect('confirm_booking', booking_id=booking.id)
                    else:
                        # If the user is authenticated but doesn't have a renter profile,
                        # redirect them to the renter profile creation form
                        messages.warning(request, "Please register a renter profile before completing your booking.")
                        return redirect(reverse('renter_registration') + f'?source=create_booking&property_id={property_id}')
                else:
                    # If the user is not authenticated, find out if they have an account, a profile, or not
                    # Redirect accordingly
                    return redirect('login_check')

            else:
                # Property is not available, handle accordingly
                messages.warning(request, message)

                context = {'form': form, 'property': property}
                return render(request, 'booking/create_booking.html', context)
    
    else:
        # Check if there's stored form data in the session
        form_data = request.session.get('booking_form_data', None)
        form = BookingForm(initial=form_data) if form_data else BookingForm()

        # Clear the session data
        if 'booking_form_data' in request.session:
            del request.session['booking_form_data']

    context = {'form': form, 'property': property}
    return render(request, 'booking/create_booking.html', context)


@login_required()
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    number_of_days = booking.get_stay_duration()
    form = ConfirmBookingForm(request.POST)

    if form.is_valid() and request.method == 'POST':
        submitted_email = form.cleaned_data['email']

        # store submitted email and context objects in session
        request.session['submitted_email'] = submitted_email

        return redirect(reverse('initiate_payment', kwargs={'booking_id': booking.id}))

    form = ConfirmBookingForm()
    context = {
            'booking': booking,
            'form': form,
            'number_of_days': number_of_days,
        }

    return render(request, 'booking/confirm_booking.html', context)



login_required()
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # If the booking hasn't been confirmed yet, just return to the listing view because the booking hasn't been saved
        if booking.confirmation_status == 'unconfirmed':
            messages.warning("You did not complete this booking. So there's no need cancelling.")
            return redirect('renter_booking_details')
        
        # If the booking is confirmed (meaning payment has also been made) but the stay duration has started running, don't cancel
        elif booking.confirmation_status == 'confirmed' and (date.today() > booking.check_in_datetime.date() or date.today() > booking.check_out_datetime.date()):
            messages.warning(request, "You cannot cancel this booking because your stay duration has started running or has expired!")
            return redirect('renter_booking_details')
        else:
            # cancel booking
            # Implement payment cancellation/refund logic here
        
            booking.confirmation_status = 'cancelled'
            booking.save()

            messages.success(request, "Booking successfully cancelled!")
            return redirect('renter_booking_details')

    return render(request, 'cancel_booking.html', {'booking': booking})



# VIEWS FOR VIEWING RENTER BOOKINGS

def is_renter(user):
    # Check if the user is both logged-in and a manager
    return user.is_authenticated and hasattr(user, 'renter')

@user_passes_test(is_renter)
def renter_bookings_view(request):
    user = request.user
    renter_profile = get_object_or_404(RenterProfile, user=user)
    bookings = Booking.objects.filter(renter=renter_profile).order_by('-check_in_datetime')

    current_bookings = []
    past_bookings = []
    for booking in bookings:
        if booking.confirmation_status == 'confirmed' or booking.confirmation_status == 'cancelled':
            if date.today() < booking.check_out_datetime.date():
                current_bookings.append(booking)
            else:
                past_bookings.append(booking)

    context = {
        'bookings': bookings,
        'current_bookings': current_bookings,
        'past_bookings': past_bookings
        }

    return render(request, 'booking/renter_bookings.html', context)


@user_passes_test(is_renter)
def renter_booking_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, 'booking/renter_booking_details.html', {'booking': booking})



# VIEWS FOR VIEWING MANAGER'S BOOKINGS

def is_manager(user):
    # Check if the user is both logged-in and a manager
    return user.is_authenticated and hasattr(user, 'manager')

@user_passes_test(is_manager)
def manager_bookings_view(request):
    user = request.user
    manager = get_object_or_404(ManagerProfile, user=user)

    properties = Property.objects.filter(property_manager=manager)
    booking = Booking.objects.filter

    bookings = []
    for property in properties:
        try:
            booking = get_object_or_404(Booking, property=property)
            bookings.append(booking)
        except:
            pass
    
    current_bookings = []
    past_bookings = []
    print(bookings)
    if bookings:
        for booking in bookings:
            if date.today() < booking.check_out_datetime.date():
                current_bookings.append(booking)
            else:
                past_bookings.append(booking)

    context = {
        'properties': properties,
        'bookings': bookings,
        'current_bookings': current_bookings,
        'past_bookings': past_bookings
    }

    return render(request, 'booking/manager_bookings.html', context)


@user_passes_test(is_manager)
def manager_booking_details(request, booking_id):
    # user = request.user
    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, 'booking/manager_booking_details.html', {'booking': booking})
