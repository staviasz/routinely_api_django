from django.db import models


class CustomerDBModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    accepted_terms = models.BooleanField(null=False)
