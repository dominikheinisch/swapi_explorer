from django.db import models


class File(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField('creation date')
