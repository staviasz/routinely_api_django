from django.db import models


class SessionDBModel(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(null=False)
    expires_at = models.DateTimeField(null=False)
    customer = models.ForeignKey(
        "CustomerDBModel", on_delete=models.CASCADE, null=False
    )
