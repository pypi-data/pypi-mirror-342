from django.db import models


class Token(models.Model):
    token = models.CharField()
    expires_in = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=255, default='1')

    def save(self, *args, **kwargs):
        # Delete all existing entries before saving a new one
        Token.objects.all().delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.token
