from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse


from .models import Response, Review
from .forms import ManagerResponseForm, RenterReviewForm
from accounts.models import ManagerProfile, RenterProfile
from property.models import Property
# from property.views import listing_details as property_listing_details

# Create your views here.


def is_renter(user):
    # Check if the user is both logged-in and a renter
    return user.is_authenticated and hasattr(user, 'renter')


def create_review(request, property_id):

    if not is_renter(request.user):
        messages.error(request, "Access Denied! You cannot leave a review on a property you haven't booked and stayed in. Start by creating a renter profile")
        return redirect('renter_registration')

    property = get_object_or_404(Property, id=property_id)
    renter = get_object_or_404(RenterProfile, user=request.user)
    
    if request.method == 'POST':
        form = RenterReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.renter = renter
            review.property = property
            review.save()

            print('success5')
            # context = {'property': property, 'review': review}

            # return property_listing_details(request, property.id, extra_context=context)
            return redirect('listing_details', listing_id=property.id)
    
    is_renter_flag = False
    bookings = property.bookings.all()
    # print(bookings)
    # if bookings:
    for booking in bookings:
        if booking.renter == renter:
            is_renter_flag = True
        else:
            is_renter_flag = False
    
    form = RenterReviewForm()
    context = {'form': form, 'is_renter_flag': is_renter_flag, 'property': property}

    return render(request, 'reviews/review.html', context)



def is_manager(user):
    # Check if the user is both logged-in and a manager
    return user.is_authenticated and hasattr(user, 'manager')


def respond_to_review(request, review_id):

    review = get_object_or_404(Review, id=review_id)
    property = review.property

    if not is_manager(request.user):
        messages.error(request, "Access Denied. Only the property manager can respond to this review.")
        return redirect(reverse('listing_details', args=[property.id]))

    if request.method == 'POST':
        form = ManagerResponseForm(request.POST)

        if form.is_valid():
            response = form.save(commit=False)
            response.review = review
            response.save()

            # context = {'property': property, 'response': response, 'review': review}

            # return property_listing_details(request, property.id, extra_context=context)
            return redirect(reverse('listing_details', args=[property.id]))

    is_manager_flag = False
    user = request.user
    manager = get_object_or_404(ManagerProfile, user=user)
    
    if review.property.property_manager == manager:
        is_manager_flag = True
    else:
        is_manager_flag = False

    form = ManagerResponseForm()
    context = {
        'form': form, 
        'is_manager_flag': is_manager_flag, 
        'review': review, 'property': property
    }

    return render(request, 'reviews/response.html', context)





# ADD A VIEW FOR VOTING HOW HELPFUL A REVIEW WAS