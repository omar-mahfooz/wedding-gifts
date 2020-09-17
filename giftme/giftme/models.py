from django.db import models

class Gift(models.Model):
    text = models.CharField(max_length=40)
    purchase = models.BooleanField(default=False)

    def __str__(self):
        return self.text