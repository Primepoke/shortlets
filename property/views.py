from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test #,, permission_required,
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .forms import ManagerRegistrationForm, RenterRegistrationForm, UserForm, PropertyForm, UserEditForm, ManagerProfileEditForm, RenterProfileEditForm

from .models import ManagerProfile, Property, RenterProfile, User
# Create your views here.

def index(request):
    # Get all the properties in reverse order of creation
    properties = Property.objects.all().order_by('-created_at')

    return render(request, 'property/index.html', {'properties': properties})



def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            registration_type = form.cleaned_data.get('registration_type')
            # registration_type = request.POST.get('registration_type')

            # Save user's details and log them in
            user.save()
            login(request, user)

            # Redirect the user based on selected profile
            if registration_type == 'manager':
                return redirect('manager_registration')
            elif registration_type == 'renter':
                return redirect('renter_registration')

            # Redirect to index page if users don't specify a profile
            return redirect('index')
    else:
        form = UserForm()

    return render(request, 'property/registration.html', {'form': form})
        

def login_view(request):
    if request.method == 'POST':

        # Attempt to sign the user in
        login_input = request.POST['login_input']
        password = request.POST['password']

        # Determine if the user used their email or username
        is_email = '@' in login_input

        # authenticate based on either email or username
        if is_email:
            user = authenticate(request, email=login_input, password=password)
        else:
            user = authenticate(request, username=login_input, password=password)

        # Check if authentication succeeded
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'property/login.html', {'message': "Invalid login credentials (username/email and password)."})

    else:
        return render(request, 'property/login.html')
    

def logout_view(request):
    logout(request)
    return redirect('index')


# RENTER VIEWS - REGISTRATION, EDIT, PROFILE PAGE, ETC

@login_required(login_url='login')
def renter_registration(request):
    user = request.user

    # Check if the user already has a renter profile
    if hasattr(user, 'renter'):
        messages.warning(request, "You already have a renter profile.")
        return redirect('index')  # Redirect to a suitable page


    if request.method == 'POST':
        form = RenterRegistrationForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)

            messages.success(request, 'Renter profile created successfully!')
            
            # Check if there is a 'source' query parameter
            source = request.GET.get('source', None)
            if source == 'create_booking':
                # If the source is 'create_booking', redirect back to create_booking
                property_id = request.GET.get('property_id', None)
                if property_id:
                    redirect_url = reverse('create_booking', kwargs={'property_id': property_id})
                    return redirect(redirect_url)
            
            # If no specific source, redirect to a default view or index page
            return redirect('index')
    else:
        form = RenterRegistrationForm()
    
    return render(request, 'property/renter_registration.html', {'form': form})


# def renter_profile(request, username):
#     user = get_object_or_404(User, username=username)
#     profile = get_object_or_404(RenterProfile, user=user)
#     renter_reviews = profile.reviews.all()
#     # renter_properties = [review.property for review in renter_reviews]
    
#     context = {
#         'profile': profile,
#         'renter_reviews': renter_reviews,
#         # 'renter_properties': renter_properties
#     }
    
#     return render(request, 'property/renter_profile.html', context)


# MANAGER VIEWS - REGISTRATION, EDIT, PROFILE PAGE, ETC

@login_required(login_url='login')
def manager_registration(request):
    user = request.user

    # Check if the user already has a manager profile
    if hasattr(user, 'manager'):
        messages.warning(request, "You already have a manager profile.")
        return redirect('index')  # Redirect to a suitable page

    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('index') #Redirect to index/home page
    else:
        form = ManagerRegistrationForm()
    
    return render(request, 'property/manager_registration.html', {'form': form})

# def manager_profile(request, username):
#     user = get_object_or_404(User, username=username)
#     profile = get_object_or_404(ManagerProfile, user=user)
#     properties = profile.properties_managed.prefetch_related('reviews__renter').all()

#     context = {
#         'profile': profile,
#         'properties': properties,
#     }

#     return render(request, 'property/manager_profile.html', context)


# View to get all profiles for manager, renter, or user.
def profile(request, username):
    user = get_object_or_404(User, username=username)

    if hasattr(user, 'manager'):
        profile = get_object_or_404(ManagerProfile, user=user)
        properties = profile.properties_managed.prefetch_related('reviews__renter').all()

        context = {
            'profile': profile,
            'manager_properties': properties,
            'template_name': 'property/manager_profile.html',
        }

    elif hasattr(user, 'renter'):
        profile = get_object_or_404(RenterProfile, user=user)
        renter_reviews = profile.reviews.all()
        # renter_properties = [review.property for review in renter_reviews]

        context = {
            'profile': profile,
            # 'renter_properties': renter_properties,
            'renter_reviews': renter_reviews,
            'template_name': 'property/renter_profile.html',
        }

    else:
        # profile = get_object_or_404(User, user=user)

        context = {
            'profile': user,
            'template_name': 'property/user_profile.html',
        }

    return render(request, context['template_name'], context)



# EDIT PROFILE VIEW

@login_required(login_url='login_view')
def profile_edit(request):
    user = request.user

    # Check if the user has a manager profile
    if hasattr(user, 'manager'):
        profile = user.manager
        profile_form = ManagerProfileEditForm(request.POST or None, instance=profile)
    # Check if the user has a renter profile
    elif hasattr(user, 'renter'):
        profile = user.renter
        profile_form = RenterProfileEditForm(request.POST or None, instance=profile)
    # User has neither manager nor renter profile
    else:
        profile = None
        profile_form = None

    user_form = UserEditForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if user_form.is_valid() and (not profile_form or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()

            return redirect('profile_detail')  # Redirect to the user's profile detail view

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'property/profile_edit.html', context)


# NEW LISTING VIEW

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

    return render(request, 'property/listing_detail.html', {'property': property})