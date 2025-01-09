from django.db import models


class AccountDBModel(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(null=False)
    customer = models.OneToOneField(
        "CustomerDBModel", on_delete=models.CASCADE, null=False
    )
