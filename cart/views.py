from django.shortcuts import redirect, render, get_object_or_404
from main.models import Product
from .cart import Cart
from django.contrib import messages


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)

    messages.success(request, f'«{product.name}» додано до кошика.')

    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('cart:cart_detail')



def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
