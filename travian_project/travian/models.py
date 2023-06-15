from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import json
from django.core.exceptions import ValidationError

User = get_user_model()

BUILDING_TYPE_CHOICES = [
        ("Resource", "Resource"),
        ("Military", "Military")
    ]


class Building(models.Model):
    name = models.CharField(_("name"), max_length=50)
    b_type = models.CharField(_("b_type"), max_length=50, choices=BUILDING_TYPE_CHOICES)
    level = models.PositiveIntegerField(_("level"), default=1)
    construction_time = models.JSONField(_("construction_time"),)
    population = models.JSONField(_("population"),)
    resource_generation_rate = models.JSONField(_("resource_generation_rate"),)

    class Meta:
        verbose_name = _("building")
        verbose_name_plural = _("buildings")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("building_detail", kwargs={"pk": self.pk})
    


class Village(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("player"),
        on_delete=models.CASCADE,
        related_name="village",
    )
    name = models.CharField(_("name"), max_length=50)
    population = models.PositiveIntegerField(_("population"), default=0)
    granary_capacity = models.PositiveIntegerField(_("granary_capacity"), default=800)
    cranny_capacity = models.PositiveIntegerField(_("cranny_capacity"), default=800)
    wood_amount = models.PositiveIntegerField(_("wood_amount"), default=750)
    iron_amount = models.PositiveIntegerField(_("iron_amount"), default=750)
    clay_amount = models.PositiveIntegerField(_("clay_amount"), default=750)
    crop_amount = models.PositiveIntegerField(_("crop_amount"), default=750)
    building = models.ManyToManyField(
        Building,
        verbose_name=_("buildings"),
        blank=True,
    )

    class Meta:
        verbose_name = _("village")
        verbose_name_plural = _("villages")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("village_detail", kwargs={"pk": self.pk})

class Resource(models.Model):
    village = models.ForeignKey(
        Village, 
        verbose_name=_("village"), 
        on_delete=models.CASCADE,
        related_name="resources",
        blank=True,
        null=True
    )
    building = models.ManyToManyField(
        Building, 
        verbose_name=_("buildings"),
        related_name="resources",
        blank=True,
    )
    generation_rate = models.PositiveIntegerField(_("generation_rate"), default=0) 

    class Meta:
        verbose_name = _("resource")
        verbose_name_plural = _("resources")


    def get_absolute_url(self):
        return reverse("resource_detail", kwargs={"pk": self.pk})
    

    