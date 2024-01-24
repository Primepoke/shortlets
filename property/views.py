from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect

from .forms import PropertyForm
from .models import Property

from accounts.models import ManagerProfile
from reviews.models import Review

# Create your views here.

def index(request):
    # Get all the properties in reverse order of creation
    properties = Property.objects.all().order_by('-created_at')

    return render(request, 'property/index.html', {'properties': properties})



def is_manager(user):
    # Check if the user is both logged-in and a manager
    return user.is_authenticated and hasattr(user, 'manager')

@user_passes_test(is_manager, login_url='manager_registration')
def new_listing(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        user = request.user

        # try:
        #     property_manager = ManagerProfile.objects.get(user=user)
        # except ManagerProfile.DoesNotExist:
        #     # Add a message and redirect to manager registration
        #     messages.warning(request, "You must be a manager to list a property.")
        #     return redirect('manager_registration')
        
        if form.is_valid():
            property = form.save(commit=False)
            property.property_manager = ManagerProfile.objects.get(user=user)
            property.save()
            form.save_m2m()  # Save the many-to-many relationships after saving the instance

            return redirect('index')
    else:
        form = PropertyForm()

    return render(request, 'property/new_listing.html', {'form': form})



def listing_details(request, listing_id):
    property = get_object_or_404(Property, id=listing_id)
    reviews = Review.objects.filter(property=property)

    if reviews:
        context = {'property': property, 'reviews': reviews}
    else:
        context = {'property': property}

    return render(request, 'property/listing_detail.html', context)