import os
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mass_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf.default import DEFAULT_FONT
from .forms import OrderForm
from .models import Order, OrderItem
from cart.cart import Cart
from django.contrib.auth.decorators import login_required


@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Кошик порожній")
        return redirect('cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            # Створення позицій замовлення
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Побудова списку товарів
            items_list = ""
            for item in cart:
                items_list += f"- {item['product'].name} (x{item['quantity']}) — {item['total_price']} грн\n"

            # Основне повідомлення
            message = (
                f'Нове замовлення №{order.id}\n\n'
                f'Ім’я: {order.name}\n'
                f'Телефон: {order.phone}\n'
                f'Email: {order.email}\n\n'
                f'Товари:\n{items_list}\n'
                f'Загальна сума: {cart.get_total_price()} грн'
            )

            # ✅ Реєстрація шрифта, якщо ще не зареєстрований
            font_path = os.path.join(os.path.dirname(
                __file__), 'fonts', 'DejaVuSans.ttf')
            if 'DejaVuSans' not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
                DEFAULT_FONT['helvetica'] = 'DejaVuSans'

            # ✅ Генерація PDF з HTML
            html = render_to_string('orders/order_invoice.html', {
                'order': order,
                'cart': cart
            })
            pdf_file = BytesIO()
            pisa.CreatePDF(html, dest=pdf_file, encoding='utf-8')
            pdf_file.seek(0)

            # 📩 Email адміну
            send_mass_mail((
                (
                    f'Нове замовлення №{order.id}',
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                   [settings.EMAIL_ADMIN],
                ),
            ))


            # 📩 Email клієнту з PDF
            email = EmailMessage(
                subject=f'Підтвердження замовлення №{order.id}',
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[order.email]
            )
            email.attach(f'invoice_{order.id}.pdf',
                         pdf_file.read(), 'application/pdf')
            email.send()

            # 🧹 Очистити кошик
            cart.clear()

            # ✅ Повідомлення + редірект
            messages.success(
                request, f'Замовлення №{order.id} успішно оформлено.'
            )
            return redirect('orders:order_success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'orders/order_form.html', {'form': form, 'cart': cart})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})
