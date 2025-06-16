from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .forms import ContactForm, OrderForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Slider, Review
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from news.models import News
from django.templatetags.static import static

# Create your views here.


def home(request):
    sliders = Slider.objects.filter(active=True).order_by('order')
    reviews = Review.objects.all().order_by('-created_at')[:5]
    popular_products = Product.objects.all()[:5]
    recent_news = News.objects.all()[:3]
    return render(request, 'main/home.html', {'sliders': sliders, 'reviews': reviews, 'popular_products': popular_products, 'recent_news': recent_news})


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    selected_category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if selected_category:
        products = products.filter(category__slug=selected_category)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'main/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # OG-зображення
    if product.image:
        og_image_url = request.build_absolute_uri(product.image.url)
    else:
        og_image_url = request.build_absolute_uri(static('img/hero.jpg'))

    return render(request, 'main/product_detail.html', {
        'product': product,
        'form': OrderForm(),  # якщо є форма
        'request': request,
        'og_image_url': og_image_url
    })


def support(request):
    return render(request, 'main/support.html')


def contact(request):
    form = ContactForm(request.POST or None)
    success = False

    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        full_message = f"Ім’я: {name}\nEmail: {email}\n\nПовідомлення:\n{message}"

        send_mail(
            subject="Повідомлення з сайту Falcon Optic",
            message=full_message,
            from_email=f"Falcon Optic <{settings.DEFAULT_FROM_EMAIL}>",
            recipient_list=['galatserega@gmail.com'],
            fail_silently=False,
        )

        success = True
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form, 'success': success})
