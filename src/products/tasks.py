from celery import shared_task
from django.apps import apps
# from products.models import Products, ProductScapeEvent
import helpers


@shared_task
def scrape_data(url=None):
    ProductScapeEvent = apps.get_model('products', 'ProductScapeEvent')
    html = helpers.scrape(url, solve_captcha=False)
    data = helpers.extract_amazon_product_data(html)
    event = ProductScapeEvent.objects.create_scrape_event(data, url=url)
    return event.id

@shared_task
def scrape_product():
    product = apps.get_model('products', 'Products')
    qs = product.objects.filter(active=True)
    for obj in qs:
        url = obj.url
        scrape_data.delay(url=url)