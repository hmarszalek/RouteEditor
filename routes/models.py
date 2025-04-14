from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class BackgroundImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/backgrounds/')

    def __str__(self):
        return self.name

class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    background = models.ForeignKey(BackgroundImage, on_delete=models.CASCADE)

    def __str__(self):
        return f"Route-of-{self.user}-{self.name}"

class RoutePoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, related_name='points', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()

    def clean(self):
        if self.x < 0 or self.y < 0:
            raise ValidationError("Coordinates must be non-negative")

    def __str__(self):
        return f"Point-of-{self.user}-on-Route-{self.route.name}-({self.x},{self.y})"
