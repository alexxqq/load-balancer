from django.db import models

# Create your models here.
class NodeModel(models.Model):
    name = models.CharField(max_length = 255)
    messages = models.IntegerField()
    date_created = models.DateTimeField()
    is_active = models.BooleanField(default = False)
