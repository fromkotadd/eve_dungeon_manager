from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


from .choices import SkillNames, SkillLevels, CoreColors, PilotRatings, FitGrade, ImplantNames, Dungeons, ShipNames


class Pilot(models.Model):
    discord_id = models.CharField(max_length=200)
    name = models.CharField(max_length=32)
    corporation = models.CharField(max_length=6)
    tech_level = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    pilot_rating = models.CharField(max_length=4, choices=PilotRatings.choices)

    def __str__(self):
        return f"discord_id: {self.discord_id}," \
               f" name: {self.name}," \
               f" corporation: {self.corporation}," \
               f" tech_level: {self.tech_level}, " \
               f"pilot_rating: {self.pilot_rating}"
class Skill(models.Model):
    pilot = models.ForeignKey('Pilot', on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50, choices=SkillNames.choices)
    level = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])


class PilotShip(models.Model):
    pilot = models.ForeignKey('Pilot', on_delete=models.CASCADE, related_name='pilot_ships')
    ship_name = models.CharField(max_length=50, choices=ShipNames.choices)
    core_color = models.CharField(max_length=50, choices=CoreColors.choices)
    core_lvl = models.PositiveSmallIntegerField(validators=[MaxValueValidator(7)])
    fit_grade = models.CharField(max_length=10, choices=FitGrade.choices)


class Implant(models.Model):
    pilot = models.ForeignKey('Pilot', on_delete=models.CASCADE, related_name='implants')
    implant_name = models.CharField(max_length=50, choices=ImplantNames.choices)
    implant_level = models.PositiveSmallIntegerField(validators=[MaxValueValidator(45)])


class Dungeon(models.Model):
    dungeon_name = models.IntegerField(unique=True, choices=Dungeons.choices)


class DungeonPilotVisit(models.Model):
    dungeon = models.ForeignKey('Dungeon', on_delete=models.CASCADE, related_name='visits')
    pilot = models.ForeignKey('Pilot', on_delete=models.CASCADE, related_name='visits')
    date_created = models.DateTimeField(auto_now_add=True)
