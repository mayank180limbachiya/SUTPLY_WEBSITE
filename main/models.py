
from django.db import models

class Quote(models.Model):
    PROJECT_TYPES = [
        ('Residential', 'Residential Project'),
        ('Commercial', 'Commercial Project'),
        ('Designer', 'Interior Designer / Architect'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPES, blank=True)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=50, default='form', help_text='form or popup')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quote Inquiry'
        verbose_name_plural = 'Quote Inquiries'

    def __str__(self):
        return f"{self.name} – {self.phone} ({self.created_at.strftime('%d %b %Y %H:%M')})"


class EmailSettings(models.Model):
    """Admin-configurable email settings for notifications."""
    owner_email = models.EmailField(help_text="Inquiry notifications will be sent here")
    send_email_on_inquiry = models.BooleanField(default=True, help_text="Toggle email notifications on/off")
    email_subject_prefix = models.CharField(max_length=100, default="[SUTPLY] New Inquiry")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Email Settings'
        verbose_name_plural = 'Email Settings'

    def __str__(self):
        return f"Email Settings → {self.owner_email}"

    def save(self, *args, **kwargs):
        # Singleton: only one row allowed
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={'owner_email': 'sutply.in@gmail.com'})
        return obj