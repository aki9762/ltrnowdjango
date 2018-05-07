# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime
import ast
import jwt
import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from roles.models import permission
from entity.models import entity

@api_view(['POST'])
#@permission_classes((IsAuthenticated, ))
def permissions(request,id):
	try:
		eId=id
		data = request.data
		entityDetail = entity.objects.get(id= eId)

		if(entityDetail!=""):
			if(data["action"]=="create"):
				permdetails = permission()		
				permdetails.entityId= eId
				permdetails.roleId=data["roleId"]
				permdetails.description= data["description"]	
				permdetails.permission= data["permission"]
				permdetails.createdBy= data["createdBy"]
				permdetails.save()

				return HttpResponse(json.dumps({"responsecode":"200","status":"Success: Created","pId":permdetails.pId}),content_type="application/json")	
			if(data["action"]=="edit"):
					permdetails = permission.objects.get(tId= data['tId'])
					permdetails.entityId= eId
					permdetails.roleId=data["roleId"]
					permdetails.description= data["description"]	
					permdetails.permission= data["permission"]			
					permdetails.modifiedBy = data["modifiedBy"]
					permdetails.save()
					return HttpResponse(json.dumps({"responsecode":"200","status":"Success: Edited","pId":permdetails.pId}),content_type="application/json")
			if(data["action"] == "alllist"):
				permdetails = permission.objects.filter(isActive=True).filter(entityId=eId)
				permList = []
				for sg in permdetails:
					obj = {"id":sg.id,"pId":sg.pId,"entityid":sg.entityId,"roleid":sg.roleId,"description":sg.description,"permission":sg.permission}
					permList.append(obj)
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Listed","permissionlist":permList}),content_type="application/json")

			if(data["action"] == "delete"):
				permdetails = permission.objects.get(tId=data['tId'])
				permdetails.isActive=False
				permdetails.save()
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Deleted"}),content_type="application/json")
		else:
			return HttpResponse(json.dumps({"responsecode":"300","status":"success","msg":"No Record Exits!!!"}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({ "status" : False, "responce_code":"500","error":str(e) }), content_type="application/json")
#---------------------------------- End API'---------------------------------------#

@api_view(['GET'])
def permissiondetailsbyId(request,id, pId):
    try:
		eId=id
		type = request.data
		entityDetail = entity.objects.get(id= eId)
		sg = permission.objects.get(entityId=eId, pId= pId)
		obj = {"id":sg.id,"pId":sg.pId,"entityid":sg.entityId,"roleid":sg.roleId,"description":sg.description,"permission":sg.permission}
		return HttpResponse(json.dumps({"responsecode":"200","status":"success: Listed","permissiondetails":obj}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"status" : "fail","msg":str(e)}), content_type = "application/json")