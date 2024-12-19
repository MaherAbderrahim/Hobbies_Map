import logging
from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from .models import Utilisateur
from .forms import UtilisateurCreationForm, UtilisateurLoginForm
from .forms import CustomPasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse 
from .utils import is_ajax,classify_face
import base64
from logs.models import Log
from django.core.files.base import ContentFile
from profiles.models import Profile
from django.contrib.auth import get_user_model
from Activity.models import Activity
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
# Register a new user
def register(request):
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('login')
        else:
            print("Form errors:", form.errors)  # Debugging
    else:
        form = UtilisateurCreationForm()
    return render(request, 'user/register.html', {'form': form})

from django.contrib.auth import login, authenticate
from .forms import UtilisateurLoginForm

def login_view(request):
    if request.method == 'POST':
        form = UtilisateurLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('user:home')  
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UtilisateurLoginForm()
    return render(request, 'user/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# List all users
@login_required
def user_list(request):
    users = Utilisateur.objects.all()
    return render(request, 'user/user_list.html', {'users': users})

# Update user details
@login_required
def update_user(request, pk):
    user = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UtilisateurCreationForm(instance=user)
    return render(request, 'user/user_form.html', {'form': form})

# Delete a user
@login_required
def delete_user(request, pk):
    user = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user/user_confirm_delete.html', {'user': user})

def index_view(request):
    return render(request, 'user/index.html')

logger = logging.getLogger(__name__)
class CustomPasswordResetView(PasswordResetView):
    template_name = 'user/password_reset_form.html'  # Form template
    email_template_name = 'user/password_reset_email.html'  # Plaintext email template
    success_url = reverse_lazy('password_reset_done')

    def get_users(self, email):
        """
        Fetch users based on the provided email address.
        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True
        )
        return [user for user in active_users if user.has_usable_password()]

    def form_valid(self, form):
        """
        Process the valid form to send custom password reset emails.
        """
        for user in self.get_users(form.cleaned_data['email']):
            # Generate the UID and token
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user) # type: ignore
            
            # Construct the reset URL
            domain = get_current_site(self.request).domain
            protocol = 'https' if self.request.is_secure() else 'http'
            reset_url = f"{protocol}://{domain}/../password_reset_confirm/{uidb64}/{token}/"
            
            # Build the email context
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': get_current_site(self.request).name,
                'uid': uidb64,
                'user': user,
                'token': token,
                'protocol': protocol,
                'custom_reset_link': reset_url,
            }

            # Log the generated reset URL
            logger.info(f"Generated reset link for user {user.email}: {reset_url}")

            # Render email content
            email_subject = _('Password Reset Requested')
            email_body = render_to_string(self.email_template_name, context)
            
            # Send email
            email = EmailMultiAlternatives(email_subject, email_body, to=[user.email])
            email.send()

        return super().form_valid(form)
    
    from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


def find_user_view(request):
    if is_ajax(request):
        photo = request.POST.get('photo')
        _, str_img = photo.split(';base64')
        decoded_file = base64.b64decode(str_img)

        x = Log()
        x.photo.save('upload.png', ContentFile(decoded_file))
        x.save()

        # Perform face classification
        res = classify_face(x.photo.path)
        User = get_user_model()

        if res:
            user_exists = User.objects.filter(email=res).exists()
            if user_exists:
                user = User.objects.get(email=res)
                profile = Profile.objects.get(user=user)
                x.profile = profile
                x.save()

                # Explicitly save the session before logging in
                request.session.save()
                login(request, user)

                # Redirect to user home after successful login
                return redirect('user:home')

        # If user is not recognized, return a failure response
        return JsonResponse({'success': False, 'error': 'User not recognized'})

    # Default response for non-AJAX requests
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def home_view(request):
    return render(request, 'user/home.html')  # Replace with your actual template


@login_required
def profile(request):
    return render(request,
                  'user/profile.html',
                  {'section': 'profile'})
    
    
    
@ login_required
def favourite_list(request):
    new = Activity.objects.filter(favourites=request.user)
    return render(request,
                  'user/favorites.html',
                  {'new': new})
    
    
@ login_required
def favourite_add(request, id):
    user = request.user
    activity = get_object_or_404(Activity, id=id)

    if activity.favourites.filter(id=user.id).exists():
        activity.favourites.remove(user)
        status = "removed"
    else:
        activity.favourites.add(user)
        status = "added"

    return JsonResponse({'status': status, 'activity_id': activity.id})