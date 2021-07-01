from django.db import models
from .utils import get_price

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=400, blank=True, null=True)
    url = models.URLField()

    product_image_url = models.URLField(max_length=200, blank=True, null=True)
    
    mrp = models.FloatField(blank=True, null=True)
    saving = models.CharField(max_length=100, blank = True, null=True)
    current_price = models.FloatField(blank=True, null=True)
    old_price  = models.FloatField(blank=True, null=True)

    price_difference = models.FloatField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('price_difference', '-created')
    
    def save(self, *args, **kwargs):
        
        (name, price, mrp, saving, img_link) = get_price(self.url)

        old_price = self.current_price
        
        if self.current_price:
            if price != old_price:
                diff = old_price - price
                self.price_difference = diff
                self.old_price = old_price
            else:
                self.old_price = 0
                self.price_difference = 0
        
        self.name = name 
        
        self.mrp = mrp 
        self.saving = saving
        
        self.current_price = price
        
        self.product_image_url = img_link

        super().save(*args, **kwargs)

  
