# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class perUUID(models.Model):
        uuidNumber = models.BigIntegerField(default=0)

# Function specifying custom id generation logic
def getPermId():
               try:
                        uuid = perUUID.objects.latest('uuidNumber')
               except Exception, e:
                        uuid = perUUID()
                        uuid.save()
               uuid.uuidNumber = uuid.uuidNumber+1
               uuid.save()
               CategoryID = 'PER'+ str(uuid.uuidNumber)
               return CategoryID
		
class permission(models.Model):
	pId=models.CharField(default=getPermId, max_length=200, unique=True)
	entityId=models.TextField(null=True,blank=True)
	roleId=models.TextField(null=True,blank=True)
	description = models.TextField(null=True,blank=True)
	permission = models.TextField(null=True,blank=True)
	isActive=models.BooleanField(default=True)
	createdBy=models.TextField(null=True,blank=True)
	modifiedBy=models.TextField(null=True,blank=True)
	createdDate=models.DateTimeField(auto_now_add=True)
	modifiedDate=models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.pId