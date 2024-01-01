from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ManagerRegistrationForm, RenterRegistrationForm, UserForm, PropertyForm

from .models import ManagerProfile, Property, User
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
            registration_type = request.POST.get('registration_type')

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


@login_required(login_url='login')
def renter_registration(request):
    user = request.user

    if request.method == 'POST':
        form = RenterRegistrationForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('index') #Redirect to index page or home
    else:
        form = RenterRegistrationForm()
    
    return render(request, 'property/renter_registration.html', {'form': form})

@login_required(login_url='login')
def manager_registration(request):
    user = request.user

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


@login_required(login_url='login')
def new_listing(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        user = request.user

        try:
            property_manager = ManagerProfile.objects.get(user=user)
        except ManagerProfile.DoesNotExist:
            error_message = "You must register a property manager profile to create a listing."
            return render(request, 'property/new_manager_profile.html', {'error_message': error_message})

        if form.is_valid():
            property = form.save(commit=False)
            property.property_manager = property_manager
            property.save()
            form.save_m2m()  # Save the many-to-many relationships after saving the instance

            return redirect('index')
    else:
        form = PropertyForm()

    return render(request, 'property/new_listing.html', {'form': form})

def listing_details(request, listing_id):
    property = get_object_or_404(Property, id=listing_id)

    return render(request, 'property/listing_detail.html', {'property': property})