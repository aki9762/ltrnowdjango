# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.
class userTypeUUID(models.Model):
        uuidNumber = models.BigIntegerField(default=0)

# Function specifying custom id generation logic
def getUserTypeId():
               try:
                        uuid = userTypeUUID.objects.latest('uuidNumber')
               except Exception, e:
                        uuid = userTypeUUID()
                        uuid.save()
               uuid.uuidNumber = uuid.uuidNumber+1
               uuid.save()
               CategoryID = 'UserTypeID-'+ str(uuid.uuidNumber)
               return CategoryID

class UserType(models.Model):
	tId=models.CharField(default=getUserTypeId, max_length=200, unique=True)
	entityId=models.TextField(null=True,blank=True)
	typeName=models.TextField(null=True,blank=True)
	description=models.TextField(null=True,blank=True)
	defaultPreference =models.TextField(null=True,blank=True)
	assignPreferences =models.TextField(null=True,blank=True)
	isActive=models.BooleanField(default=True)
	createdBy=models.TextField(null=True,blank=True)
	modifiedBy=models.TextField(null=True,blank=True)
	createdDate=models.DateTimeField(auto_now_add=True)
	modifiedDate=models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.typeName
		
# Create your models here.
class userUUID(models.Model):
        uuidNumber = models.BigIntegerField(default=0)

# Function specifying custom id generation logic
def getUserId():
               try:
                        uuid = userUUID.objects.latest('uuidNumber')
               except Exception, e:
                        uuid = userUUID()
                        uuid.save()
               uuid.uuidNumber = uuid.uuidNumber+1
               uuid.save()
               CategoryID = 'UserID-'+ str(uuid.uuidNumber)
               return CategoryID

class Users(models.Model):
	uId=models.CharField(default=getUserId, max_length=200, unique=True)
	entityId=models.TextField(null=True,blank=True)
	userType=models.TextField(null=True,blank=True)
	name=models.TextField(null=True,blank=True)
	# parentUserName = models.ForeignKey(User,to_field='username',max_length=100, null=True)
	emailid =models.EmailField(unique=True, null=True)
	# password =models.ForeignKey(User,to_field='p',max_length=100)
	isExtrafield=models.BooleanField(default=False)
	status =models.TextField(null=True,blank=True)
	switchrole =models.BooleanField(default=False)
	primaryrole =models.TextField(null=True,blank=True)
	secondaryrole =models.TextField(null=True,blank=True)
	isActive=models.BooleanField(default=True)
	createdDate=models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.name
		
class resetpassword(models.Model):
	uId=models.ForeignKey(Users,to_field='uId',max_length=100, null=True)
	resetlink=models.TextField(null=True,blank=True)
	isActive=models.BooleanField(default=True)
	createdDate=models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.uId_id

class emailverify(models.Model):
	uId=models.ForeignKey(Users,to_field='uId',max_length=100, null=True)
	verifylink=models.TextField(null=True,blank=True)
	isVerify=models.BooleanField(default=False)
	isActive=models.BooleanField(default=True)
	createdDate=models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.uId_id
		
class UsersExtrafield(models.Model):
	uId=models.ForeignKey(Users,to_field='uId',max_length=100, null=True)
	extrafield=models.TextField(null=True,blank=True)
	isActive=models.BooleanField(default=True)
	createdBy=models.TextField(null=True,blank=True)
	modifiedBy=models.TextField(null=True,blank=True)
	createdDate=models.DateTimeField(auto_now_add=True)
	modifiedDate=models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.uId

class userFileUUID(models.Model):
        uuidNumber = models.BigIntegerField(default=0)

# Function specifying custom id generation logic
def getuserFileId():
               try:
                        uuid = userFileUUID.objects.latest('uuidNumber')
               except Exception, e:
                        uuid = userFileUUID()
                        uuid.save()
               uuid.uuidNumber = uuid.uuidNumber+1
               uuid.save()
               CategoryID = 'FileID-'+ str(uuid.uuidNumber)
               return CategoryID
		
class UsersFiles(models.Model):
	fId=models.CharField(default=getuserFileId, max_length=200, unique=True)
	uId=models.ForeignKey(Users,to_field='uId',max_length=100, null=True)
	filename=models.TextField(null=True,blank=True)
	file = models.FileField(blank=False, null=False)
	isActive=models.BooleanField(default=True)
	createdBy=models.TextField(null=True,blank=True)
	modifiedBy=models.TextField(null=True,blank=True)
	createdDate=models.DateTimeField(auto_now_add=True)
	modifiedDate=models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.uId