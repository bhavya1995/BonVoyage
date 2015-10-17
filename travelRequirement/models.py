from django.db import models
from django.contrib.auth.models import User
from bonvoyage.settings import MEDIA_ROOT
import datetime
import os

# Create your models here.

class UserDetails(models.Model):

	typeClass = (
		('Traveller', 'Traveller'),
		('Travel-Agent', 'Travel-Agent'),
		('Admin', 'Admin')
	)
	type = models.CharField(max_length = 20, choices = typeClass)
	user = models.OneToOneField(User)
	is_verified = models.BooleanField(default = False)

	def __str__(self):
		return (str(self.user.first_name) + " " + str(self.user.last_name) + " " + str(self.type));	

class travelReq (models.Model):
	userId = models.ForeignKey(User);
	startDate = models.CharField(max_length= 255, null = True, blank = True)
	endDate = models.CharField(max_length= 255, null = True, blank = True)
	budget = models.CharField(null = True, max_length = 255)
	reqName = models.CharField(null = True, max_length = 255, default = "MyPackage")
	placeToVisit = models.CharField(null = True, blank = True, max_length = 255)
	status=models.BooleanField(default=False)
	def __str__(self):
		return str(self.userId.username);

class travelPackage (models.Model):
	travelReqId= models.ForeignKey (travelReq)	
	userId = models.ForeignKey (User)
	name = models.CharField (null = True, blank = True, max_length = 255)
	price = models.CharField (null = True, blank = True, max_length = 255)
	bidPrice = models.CharField (null = True, blank = True, max_length = 255,default=0)
	remarks = models.CharField(max_length = 255, null = True,default="The Place is truly awesome with great food and good quality people")
	selectedForBid = models.BooleanField(default=False)
	selectedByTraveller = models.BooleanField(default=False)

	def __str__(self):
		return (self.name + " " + str(self.userId));	

class daysSch (models.Model):
	dayNum = models.CharField(max_length = 255)	
	description = models.CharField(max_length = 255, null = True)
	travelPackageId = models.ForeignKey(travelPackage)

	def __str__(self):
		return (str(self.dayNum) + " " + str(self.description));

class hotelDetails (models.Model):
	name = models.CharField(max_length = 255)
	place = models.CharField(max_length = 255)
	roomType = models.CharField (max_length = 255)
	numOfDays = models.CharField(max_length = 255, null = True)
	travelPackageId = models.ForeignKey(travelPackage)

	def __str__(self):
		return str(self.name);

class airportDetails (models.Model):
	name = models.CharField(max_length = 255, null = True)
	city = models.CharField(max_length = 255, null = True)
	country = models.CharField(max_length = 255, null = True)
	code = models.CharField(max_length = 255, null = True)

	def __str__(self):
		return str(self.name);


class flightDetails (models.Model):
	typeClass = (
		('Economic', 'Economic'),
		('Business', 'Business'),
		('First Class', 'First Class')
	)
	fromPlace = models.CharField(max_length = 255, null = True)
	toPlace = models.CharField(max_length = 255, null = True)
	type = models.CharField(max_length = 20, choices = typeClass)
	travelPackageId = models.ForeignKey(travelPackage)

	def __str__(self):
		return str(self.travelPackageId);

class isoCode (models.Model):
	country = models.CharField(max_length = 255, null = True)
	code = models.CharField(max_length = 255, null = True)

	def __str__(self):
		return str(self.country);

class feedback (models.Model):
	userId = models.ForeignKey(User)
	agentId = models.CharField(max_length=10,blank=True,null=True,default="None")
	userReqId = models.ForeignKey(travelReq,blank=True,null=True)
	agentRating = models.IntegerField (blank=True,null=True,default=0)
	agentReview = models.CharField (max_length=255,blank=True, null=True,default="Blank")

class feedback_files (models.Model):
	fileUpload = models.FileField(upload_to = MEDIA_ROOT)
	feedbackId = models.ForeignKey(feedback)

class agent_files (models.Model):
	fileUpload = models.FileField(upload_to = MEDIA_ROOT)
	userId = models.ForeignKey(User)

	def filename(self):
		return os.path.basename(self.fileUpload.name)

class agent_details (models.Model):
	userId = models.ForeignKey(User)
	licenceNum = models.CharField(max_length = 255, null = True)
	panNum = models.CharField(max_length = 255, null = True)
	name = models.CharField(max_length = 255, null = True)
	fathersName = models.CharField(max_length = 255, null = True)
	address = models.CharField(max_length = 255, null = True)
	dob = models.CharField(max_length = 255, null = True)
	namePan = models.CharField(max_length = 255, null = True)
	fathersNamePan = models.CharField(max_length = 255, null = True)
	dobPan = models.CharField(max_length = 255, null = True)

class destination (models.Model):

	type=models.CharField(max_length=30,blank=True,null=True)
	name=models.CharField(max_length=30,blank=True,null=True)
	image=models.FileField(upload_to = MEDIA_ROOT)

	def filename(self):
		return os.path.basename(self.fileUpload.name)

