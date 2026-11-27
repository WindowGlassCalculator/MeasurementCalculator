from django.db import models


class CalculationHistory(models.Model):

    width = models.CharField(max_length=20)
    height = models.CharField(max_length=20)

    bearing_patti = models.CharField(max_length=20)
    handle_interlock = models.CharField(max_length=20)

    glass_bearing_patti = models.CharField(max_length=20)
    glass_handle_interlock = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Width: {self.width}, Height: {self.height}"