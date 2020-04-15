from django.db import models

class Thing(models.Model):
    name = models.CharField("name", max_length=32, unique=True)
