from django.db import models


class QueueModel(models.Model):
    name = models.CharField(null=False, max_length=120)
    password = models.CharField(null=False, max_length=120)
    ids = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
