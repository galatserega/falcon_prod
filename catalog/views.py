import os
from io import BytesIO
from collections import defaultdict

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.staticfiles import finders

from weasyprint import HTML, CSS
from main.models import Product


def download_catalog(request):
    products = Product.objects.select_related('category')
    products_list = []

    # Повний шлях до папки з фото
    image_dir = os.path.join(settings.BASE_DIR, 'products')

    for product in products:
        product_dict = {
            'name': product.name,
            'short_description': product.short_description,
            'price': product.price,
        }

        if product.image:
            image_filename = os.path.basename(product.image.name)
            full_image_path = os.path.join(image_dir, image_filename)
            if os.path.exists(full_image_path):
                product_dict['image_full_path'] = 'file:///' + \
                    full_image_path.replace('\\', '/')

        products_list.append(product_dict)

    context = {
        'products': products_list,
        'logo_path': finders.find('images/logo.png'),
        'font_path': finders.find('fonts/DejaVuSans.ttf'),
        'current_date': timezone.now().strftime('%d.%m.%Y'),
    }

    html_string = render_to_string('main/pdf_catalog.html', context)
    css_path = finders.find('css/pdf.css')

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(
        pdf_file,
        stylesheets=[CSS(filename=css_path)] if css_path else None
    )

    response = HttpResponse(pdf_file.getvalue(),
                            content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="catalog.pdf"'
    return response
