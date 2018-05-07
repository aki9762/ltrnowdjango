# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
import os

from django.db import models

# Create your models here.
#--------------decide the path of uploded file --------------------------#
def get_upload_filepath(self, filename):
  directory =settings.MEDIA_ROOT+"/"+"WebsiteDocuments" #D:\Local Python Projects\lms\WebsiteDocuments
  if not os.path.exists(directory):
    os.makedirs(directory)
  full_path = str(directory)+"/%s" %(filename)
  print "full_path --> ",full_path
  return full_path
#------------------------------------------------------------------------#

#----------------------- Start entity -------------------------#

class entityUUID(models.Model):
        uuidNumber = models.BigIntegerField(default=0)


# Function specifying custom id generation logic
def getentityId():
               try:
                        uuid = entityUUID.objects.latest('uuidNumber')
               except Exception, e:
                        uuid = entityUUID()
                        
               uuid.uuidNumber = uuid.uuidNumber + 1
               entityID = 'entityID-'+ str(uuid.uuidNumber)
               uuid.save()
               
               return entityID

class entity(models.Model):
	eId=models.CharField(default=getentityId, max_length=200, unique=True)
	entityName=models.TextField(null=True,blank=True)
	domain=models.TextField(null=True,blank=True)
	emailid=models.TextField(null=True,blank=True)
	logo=models.FileField(upload_to=get_upload_filepath,null=True, blank=True,max_length=500)
	status=models.TextField(null=True,blank=True)
	isActive=models.BooleanField(default=True)
	createdBy=models.TextField(null=True,blank=True)
	modifiedBy=models.TextField(null=True,blank=True)
	createdDate=models.DateTimeField(auto_now_add=True)
	modifiedDate=models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.entityName

#----------------------- End entity -------------------------#