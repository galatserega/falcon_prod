# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # ВАЖЛИВО: неактивний поки не підтвердить email
            user.save()

            # Генеруємо токен
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            verify_url = f"http://{domain}/accounts/verify-email/{uid}/{token}/"

            # Лист
            subject = 'Підтвердження вашої електронної адреси'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'verify_url': verify_url,
            })

            send_mail(subject, message, None, [user.email])

            return render(request, 'accounts/registration_pending.html')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:profile')
    else:
        return HttpResponse('Посилання недійсне або застаріле.')

    
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

