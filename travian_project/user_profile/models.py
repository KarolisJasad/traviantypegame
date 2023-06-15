from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='profile',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})