from django.db import models

from products.tasks import scrape_data

# Create your models here.
class Products(models.Model):
    asin = models.CharField(max_length=120, unique=True, db_index=True)
    url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price_raw = models.CharField(max_length=20)
    price_text = models.CharField(max_length=20)
    price = models.FloatField(default=0.0, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, help_text="scape daily?")
    
    def __str__(self):
        return self.title
    
    
class ProductScapeEventManger(models.Manager):
    def create_scrape_event(self, data, url=None):
        asin = data.get('asin') or None
        
        if not asin:
            return None
        product, created = Products.objects.update_or_create(asin=asin, defaults={
            "url": data.get('url') or None,
            "title": data.get('title') or "",
            "price": data.get('price') or 0.0,
            "description": data.get('description') or "",
        })
        
        event = self.create(product=product, 
            asin=asin, metadata=data, url=url)
        return event
        
class ProductScapeEvent(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product_scape_events")
    asin = models.CharField(max_length=20)
    url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=100)
    metadata = models.JSONField()
    # price_raw = models.CharField(max_length=20)
    # price_text = models.CharField(max_length=20)
    # price = models.FloatField()
    # description = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    objects = ProductScapeEventManger()
    
