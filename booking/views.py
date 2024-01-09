from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Booking
from .forms import BookingForm, LoginCheckForm, AvailabilityForm
from .utils import is_property_available
from decimal import Decimal

from property.models import Property #, RenterProfile
from property.forms import RenterRegistrationForm #, UserForm

# Create your views here.



def check_availability(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if start_date > end_date:
                messages.warning(request, "Start date should be before end date.")
                return redirect(reverse('check_availability', args=[property_id]))

            if is_property_available(property, start_date, end_date):
                messages.success(request, f"This property is Available for Booking from {start_date.isoformat()} to {end_date.isoformat()}. BOOK NOW!")
                return redirect(reverse('listing_details', args=[property_id]))
            else:
                messages.warning(request, f"This property is not available from {start_date.isoformat()} to {end_date.isoformat()}.")
                return redirect(reverse('listing_details', args=[property_id]))
    else:
        form = AvailabilityForm()

    return render(request, 'booking/check_availability.html', {'property': property, 'form': form})



def login_check(request):
    if request.method == 'POST':
        user = request.user
        print(user)
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
            start_date = form.cleaned_data['check_in_date']
            end_date = form.cleaned_data['check_out_date']

            # Call the availability check function
            if is_property_available(property, start_date, end_date):
                # Property is available, continue with booking process
                booking = form.save(commit=False)
                booking.property = property

                # Store form data in the session
                form_data = form.cleaned_data
                form_data['check_in_date'] = form_data['check_in_date'].isoformat()
                form_data['check_out_date'] = form_data['check_out_date'].isoformat()
                request.session['booking_form_data'] = form_data

                if user.is_authenticated:
                    # If the user is authenticated, check for a renter profile
                    if hasattr(user, 'renter'):
                        booking.renter = user.renter
                        booking.get_total_price()
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
                booked_start_date = property.bookings.check_in_date
                booked_end_date = property.bookings.check_out_date
                messages.warning(request, f"This property is Not Available from {booked_start_date.isoformat()} to {booked_end_date.isoformat()}. Please choose different dates.")

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



def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    number_of_days = booking.get_number_of_days()
    booking.get_total_price()

    if request.method == 'POST':
        # Implement payment logic here

        # Dummy code to use for testing the booking and confirmation process
        messages.success(request, "payment successful. Booking successful")

        booking.is_confirmed = True
        booking.save()
        # print(booking)
        return redirect(reverse('listing_details', args=[booking.property.id]))

    context = {
        'booking': booking,
        'number_of_days': number_of_days,
    }
    return render(request, 'booking/confirm_booking.html', context)



def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Implement cancellation logic here
        booking.is_confirmed = False
        booking.save()
        return redirect('booking_cancellation_confirmation', booking_id=booking.id)

    return render(request, 'cancel_booking.html', {'booking': booking})