from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    image = models.URLField(max_length=1000)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
