from django.db import models


class SkillNames(models.TextChoices):
	SMALL_LASER = 'small laser'
	MEDIUM_LASER = 'medium laser'
	LARGE_LASER = 'large laser'
	CAPITAL_LASER = 'capital laser'

	SMALL_RAILGUN = 'small railgun'
	MEDIUM_RAILGUN = 'medium railgun'
	LARGE_RAILGUN = 'large railgun'
	CAPITAL_RAILGUN = 'capital railgun'

	SMALL_CANNON = 'small cannon'
	MEDIUM_CANNON = 'medium cannon'
	LARGE_CANNON = 'large cannon'
	CAPITAL_CANNON = 'capital cannon'

	SMALL_MISSILE = 'small missile'
	MEDIUM_MISSILE = 'medium missile'
	LARGE_MISSILE = 'large missile'
	CAPITAL_MISSILE = 'capital missile'

	SMALL_DRONE = 'small drone'
	MEDIUM_DRONE = 'medium drone'
	LARGE_DRONE = 'large drone'
	DRONE = 'drone'

	LIGHT_FIGHTER = 'light_fighter'
	FIGHTER = 'fighter'

	SHIELD_OPERATION = 'shield operation'

	FRIGATE_COMMAND = 'frigate command'
	FRIGATE_DEFENSE_UPGRADE = 'frigate defense upgrade'
	FRIGATE_ENGINEERING = 'frigate engineering'

	DESTROYER_COMMAND = 'destroyer command'
	DESTROYER_DEFENSE_UPGRADE = 'destroyer defense upgrade'
	DESTROYER_ENGINEERING = 'destroyer engineering'

	CRUISER_COMMAND = 'cruiser command'
	CRUISER_DEFENSE_UPGRADE = 'cruiser defense upgrade'
	CRUISER_ENGINEERING = 'cruiser engineering'

	BATTLECRUISER_SHIP_COMMAND = 'battlecruiser command'
	BATTLECRUISER_DEFENSE_UPGRADE = 'battlecruiser defense upgrade'
	BATTLECRUISER_ENGINEERING = 'battlecruiser engineering'

	BATTLESHIP_COMMAND = 'battleship command'
	BATTLESHIP_DEFENSE_UPGRADE = 'battleship defense upgrade'
	BATTLESHIP_ENGINEERING = 'battleship engineering'

	DREADNOUGHT_COMMAND = 'dreadnought command'
	DREADNOUGHT_DEFENSE_UPGRADE = 'dreadnought defense upgrade'
	DREADNOUGHT_ENGINEERING = 'dreadnought engineering'

	CARRIER_COMMAND = 'carrier command'
	CARRIER_DEFENSE_UPGRADE = 'carrier defense upgrade'
	CARRIER_ENGINEERING = 'carrier engineering'

	TARGET_MANAGEMENT = 'target management'


class SkillLevels(models.TextChoices):
	LOW = '4-4'
	MID = '4-5-3'
	HIGH = '5-5-4'


class CoreColors(models.TextChoices):
	GREEN = 'green'
	BLUE = 'blue'
	VIOLET = 'violet'
	GOLD = 'gold'
	NONE = 'none'


class FitGrade(models.TextChoices):
	grade_c = 'C'
	grade_b = 'B'
	grade_a = 'A'
	grade_x = 'X'


class ImplantNames(models.TextChoices):
	# LASER IMPLANT
	FOCUSED_CRYSTAL = 'focused crystal'
	PULSE_CRYSTAL = 'pulse crystal'

	# RAILGUN IMPLANT
	HIGH_POWER_COIL = 'high power coil'
	THERMAL_CIRCULATION = 'thermal circulation'

	# CANNON IMPLANT
	BARRAGE_REPRESSION = 'barrage repression'
	SNIPING_TECHNOLOGY = 'sniping technology'

	# MISSILE IMPLANT
	WARHEAD_CHARGE = 'warhead charge'
	TACTICAL_MISSILES = 'tactical missiles'

	# CARRIER IMPLANT
	AUTHOMATIC_DEFENSE = 'authomatic defense'
	BOMBARD_TACTICS = 'bombard tactics'


class Dungeons(models.IntegerChoices):
	I = 1, '1'
	II = 2, '2'
	III = 3, '3'
	IV = 4, '4'
	V = 5, '5'


class ShipNames(models.TextChoices):
	# 1
	VINDICATOR = 'vindicator'
	BHAAlGORN = 'bhaalgorn'
	NIGHTMARE = 'nightmare'

	# 2
	APOCALYPSE_STRIKER = 'apocalypse striker'
	APOCALYPSE_NAVY_ISSUE = 'apocalypse navy issue'

	MEGATHRON_STRIKER = 'megathron striker'
	MEGATHRON_NAVY_ISSUE = 'megathron navy issue'


	# 3-4
	PHOENIX = 'phoenix'
	NAGLFAR = 'naglfar'
	REVELATION = 'revelation'
	MOROS = 'moros'
	CHIMERA = 'chimera'
	NIDHOUGGUR = 'nidhouggur'
	ARCHON = 'archon'
	THANATOS = 'thanatos'

	# 5 bk / frigi
	NAGA = 'naga'
	TORNADO = 'tornado'
	ORACLE = 'oracle'
	HURRICANE_LOGISTICS = 'hurricane logistics'
	GARMUR = 'garmur'
	CONDOR = 'condor'
	SLASHER = 'slasher'
	EXECUTIONER = 'executioner'
	ATRON = 'atron'
