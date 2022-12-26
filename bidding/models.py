from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator


from store.models import Product


class Bid(models.Model):
    product = models.ForeignKey(Product,
                                related_name='Bid_product',
                                on_delete=models.CASCADE)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='Bid_user')
    
    bidding_amount = models.DecimalField(max_digits=15, decimal_places=2)


class Auto_bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='auto_bid_user')
    
    products = models.ManyToManyField(Product)
        
    bidding_max_amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    
    amout_left = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    bidding_notification_threshold = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(100)])
