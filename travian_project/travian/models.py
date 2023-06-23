from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from decimal import Decimal
from django.core.exceptions import ValidationError
from PIL import Image
from tinymce.models import HTMLField

User = get_user_model()

BUILDING_TYPE_CHOICES = [
    ("Resource", "Resource"),
    ("Military", "Military"),
    ("Infrastructure", "Infrastructure")
]

TROOP_TYPE_CHOICES = [
    ("Infantry", "Infantry"),
    ("Cavalry", "Cavalry")
]

LEVEL_CHOICES = [
    (1, "Level 1"),
    (2, "Level 2"),
    (3, "Level 3"),
    (4, "Level 4"),
    (5, "Level 5"),
    (6, "Level 6"),
    (7, "Level 7"),
    (8, "Level 8"),
    (9, "Level 9"),
    (10, "Level 10"),
]


class Building(models.Model):
    name = models.CharField(_("name"), max_length=50)
    b_type = models.CharField(_("b_type"), max_length=50, choices=BUILDING_TYPE_CHOICES)
    level = models.PositiveIntegerField(_("level"), choices=LEVEL_CHOICES, default=1)
    construction_time = models.JSONField(_("construction_time"),)
    population = models.JSONField(_("population"),)
    resource_generation_rate = models.JSONField(_("resource_generation_rate"),)
    building_cost = models.JSONField(_("building_cost"),)
    extra_attributes = models.JSONField(_("extra_attributes"), blank=True, null=True)
    description = models.TextField(_("description"), max_length=1000, blank=True, null=True)
    picture = models.ImageField(_("picture"), upload_to="building_pictures", blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("building")
        verbose_name_plural = _("buildings")

    def __str__(self):
        return f"{self.name} - {self.level}"

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
    warehouse_capacity = models.PositiveIntegerField(_("cranny_capacity"), default=800)
    wood_amount = models.DecimalField(_("wood_amount"), max_digits=10, decimal_places=2, default=Decimal('750.00'))
    clay_amount = models.DecimalField(_("clay_amount"), max_digits=10, decimal_places=2, default=Decimal('750.00'))
    iron_amount = models.DecimalField(_("iron_amount"), max_digits=10, decimal_places=2, default=Decimal('750.00'))
    crop_amount = models.DecimalField(_("crop_amount"), max_digits=10, decimal_places=2, default=Decimal('750.00'))
    building = models.ManyToManyField(
        Building,
        through="VillageBuilding",
        verbose_name=_("buildings"),
        blank=True,
        related_name='buildings'
    )

    class Meta:
        ordering = ['name']
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


class Troop(models.Model):
    name = models.CharField(_("name"), max_length=50)
    t_type = models.CharField(_("t_type"), max_length=50, choices=TROOP_TYPE_CHOICES, blank=True, null=True)
    attack = models.PositiveIntegerField(_("attack"), default=0)
    defense = models.PositiveIntegerField(_("defense"), default=0)
    cavalry_defense = models.PositiveIntegerField(_("cavalry_defense"), default=0)
    carrying_capacity = models.PositiveIntegerField(_("carrying_capacityi"), default=0)
    crop_consumption = models.PositiveIntegerField(_("crop_consumption"), default=0)
    construction_cost = models.JSONField(_("construction_cost"), blank=True, null=True)
    construction_time = models.JSONField(_("construction_time"), blank=True, null=True)
    description = models.TextField(_("description"), max_length=1000, blank=True, null=True)
    picture = models.ImageField(_("picture"), upload_to="building_pictures", blank=True, null=True)

    class Meta:
        verbose_name = _("troop")
        verbose_name_plural = _("troops")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("troop_detail", kwargs={"pk": self.pk})


class VillageBuilding(models.Model):
    village = models.ForeignKey(
        Village,
        on_delete=models.CASCADE,
        related_name='village_buildings'
    )
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='building_villages'
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='village_resources',
        blank=True, null=True
    )

    name = models.CharField(_("name"), max_length=100)
    level = models.IntegerField(default=1)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.village} - {self.building}"


class VillageTroop(models.Model):
    village = models.ForeignKey(
        Village,
        on_delete=models.CASCADE,
        related_name='village_troops'
    )
    troop = models.ForeignKey(
        Troop,
        on_delete=models.CASCADE,
        related_name='village_troops'
    )
    quantity = models.PositiveIntegerField(_("quantity"), default=0)

    class Meta:
        verbose_name = _("villageTroop")
        verbose_name_plural = _("villageTroops")

    def __str__(self):
        return self.troop.name

    def get_absolute_url(self):
        return reverse("villageTroop_detail", kwargs={"pk": self.pk})
