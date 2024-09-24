from django.db import models
from django.contrib.auth.models import User
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=127)
    price = models.PositiveIntegerField()
    description = models.TextField()
    items_purchased = models.PositiveIntegerField(default=0)
    rating = models.PositiveSmallIntegerField(default=0)

    #derived attribute
    @property
    def recommended(self):
        return self.rating > 4.5
