from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=127)
    price = models.PositiveIntegerField()
    description = models.TextField()
    items_purchased = models.PositiveIntegerField(default=0)
    rating = models.PositiveSmallIntegerField(default=0)

    #derived attribute
    @property
    def recommended(self):
        return self.rating > 4.5
