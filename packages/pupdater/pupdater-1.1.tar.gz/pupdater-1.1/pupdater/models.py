from django.db import models

class PipFreezeSnapshot(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, blank=True)
    raw_data = models.JSONField()

    def __str__(self):
        return self.created.strftime("%Y-%m-%d %H:%M")
    
    class Meta:
        verbose_name_plural = "Pip manager"

class RequirementsCheck(models.Model):
    note = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"RequirementsCheck {self.id}"

    class Meta:
        verbose_name_plural = "Requirements Check"
