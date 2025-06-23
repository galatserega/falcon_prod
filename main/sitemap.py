from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'product_list', 'news_list', 'support', 'contact', 'faq', 'delivery_payment']

    def location(self, item):
        return reverse(item)
