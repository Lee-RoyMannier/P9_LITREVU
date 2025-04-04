from PIL import Image
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def resize_photo(self):
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)
            img = img.resize((200, 300))
            img.save(img_path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_photo()

    class Meta:
        ordering = ['-time_created']
        verbose_name = 'Ticket'