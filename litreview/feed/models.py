from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from PIL import Image


class Ticket(models.Model):
    """ Ticket model """
    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (400, 400)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def __str__(self):
        return f'{self.title}'


class Review(models.Model):
    """ Review model """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.fields.TextField(max_length=8192, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline
