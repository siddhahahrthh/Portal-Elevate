from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from home.models import *

class CustomUserManager(BaseUserManager):
    def create_superuser(self, team_name, password=None):
        team = self.model(team_name=team_name, is_staff=True, is_superuser=True)
        team.set_password(password)
        team.save()
        return team



class Team(AbstractUser):
	"""docstring for User"""
	username			= None
	team_name			= models.CharField(max_length=50, unique=True)
	email1 				= models.EmailField(verbose_name='Email Address', unique=True, null=False, blank=False)
	name1 				= models.CharField(max_length=50)
	contact_no1 		= PhoneNumberField(blank=False, null=False, help_text='Add country code before the contact no.')
	email2 				= models.EmailField(verbose_name='Email Address', unique=True, null=False, blank=False)
	name2 				= models.CharField(max_length=50)
	contact_no2 		= PhoneNumberField(blank=False, null=False, help_text='Add country code before the contact no.')
	email3 				= models.EmailField(verbose_name='Email Address', null=True, blank=True)
	name3 				= models.CharField(max_length=50, null=True, blank=True)
	contact_no3 		= PhoneNumberField(blank=True, null=True, help_text='Add country code before the contact no.')
	email4 				= models.EmailField(verbose_name='Email Address', null=True, blank=True)
	name4 				= models.CharField(max_length=50, null=True, blank=True)
	contact_no4 		= PhoneNumberField(blank=True, null=True, help_text='Add country code before the contact no.')
	industry			= models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
	ecoins				= models.IntegerField(default=85000)

	USERNAME_FIELD 		= 'team_name'
	user_permissions 	= None
	groups 				= None
	REQUIRED_FIELDS 	= []

	objects = CustomUserManager()

	def __str__(self):
		return self.team_name


class RawMaterialCart(models.Model):
	team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
	spot = models.ForeignKey(Spot, verbose_name="Location", on_delete=models.PROTECT, null=True, blank=True)
	raw_material = models.ForeignKey(Item, limit_choices_to={'raw_material':True} ,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)

	def __str__(self):
		return str(self.team_name) + " -> " + str(self.raw_material.name)

class RawMaterialBuy(models.Model):
	team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
	spot = models.ForeignKey(Spot, on_delete=models.PROTECT, null=True, blank=True)
	raw_material_1 = models.ForeignKey(Item, related_name="RawMaterial1", limit_choices_to={'raw_material':True} ,on_delete=models.CASCADE)
	quantity_1 = models.IntegerField(default=0)
	raw_material_2 = models.ForeignKey(Item, related_name="RawMaterial2", limit_choices_to={'raw_material':True} ,on_delete=models.CASCADE)
	quantity_2 = models.IntegerField(default=0)
	raw_material_3 = models.ForeignKey(Item, related_name="RawMaterial3", limit_choices_to={'raw_material':True}, on_delete = models.CASCADE, null=True, blank=True)
	quantity_3 = models.IntegerField(default=0, null=True, blank=True)
	raw_material_4 = models.ForeignKey(Item, related_name="RawMaterial4", limit_choices_to={'raw_material':True}, on_delete = models.CASCADE, null=True, blank=True)
	quantity_4 = models.IntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return str(self.team_name) + " -> " + str(self.raw_material_1.name) + " and " + str(self.raw_material_2.name) 

class ProductCart(models.Model):
	team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
	product = models.ForeignKey(Item, limit_choices_to={'product':True}, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)

	def __str__(self):
		return str(self.team_name) + " -> " + str(self.product.name)

class SendRequest(models.Model):
	from_team = models.ForeignKey(Team, related_name="FromTeam", on_delete=models.CASCADE)
	to_team = models.ForeignKey(Team, related_name="ToTeam", on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	cost = models.IntegerField(verbose_name="Cost Per Unit")
	quantity = models.IntegerField()
	is_accepted = models.BooleanField(default=False)
	is_visible = models.BooleanField(default=False)

	def __str__(self):
		return str(self.from_team.team_name) + " -> " + str(self.to_team.team_name)


class SellUs(models.Model):
	team = models.ForeignKey(Team, on_delete=models.PROTECT)
	item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
	quantity = models.IntegerField()


