# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
#import requests
import datetime
import ast
import jwt
import requests
import string
import random

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from users.models import UserType, Users, UsersExtrafield, UsersFiles, resetpassword, emailverify
from entity.models import entity

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
# from smtplib  import SMTP_SSL,SMTPEXCEPTION
from email.header  import Header

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.base import MIMEBase
from email import Encoders

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
	
def sendmail(to, sub, msgs):
		gmail_user = 'team.solarissoftlabs@gmail.com'
		to = to
		gmail_pwd='Solaris@2018'
		subject= sub
		message = msgs
		msg = MIMEMultipart()
		msg['From'] = gmail_user
		msg['To'] =  to
		msg['Subject'] = subject
		msg.attach(MIMEText(message))
		part = MIMEBase('application', 'octet-stream')
		Encoders.encode_base64(part)
		mailServer = smtplib.SMTP('smtp.gmail.com:587')
		mailServer.starttls()
		mailServer.login(gmail_user, gmail_pwd)
		mailServer.sendmail(gmail_user, to, msg.as_string())
		mailServer.close()	
		return '1'

# Create your views here.
@api_view(['POST'])
#@permission_classes((IsAuthenticated, ))
def usertype(request,id):
	try:
		eId=id
		data = request.data
		entityDetail = entity.objects.get(id= eId)

		if(entityDetail!=""):
			if(data["action"]=="create"):
				usertypeDetail = UserType()		
				usertypeDetail.entityId= eId
				usertypeDetail.typeName=data["typeName"]
				usertypeDetail.description= data["description"]	
				usertypeDetail.defaultPreference= data["defaultPreference"]	
				usertypeDetail.assignPreferences= data["assignPreferences"]	
				usertypeDetail.createdBy= data["createdBy"]
				usertypeDetail.save()

				return HttpResponse(json.dumps({"responsecode":"200","status":"Success: Created","tId":usertypeDetail.tId}),content_type="application/json")	
			if(data["action"]=="edit"):
					usertypeDetail = UserType.objects.get(tId= data['tId'])
					usertypeDetail.entityId= eId
					usertypeDetail.typeName=data["typeName"]
					usertypeDetail.description= data["description"]	
					usertypeDetail.defaultPreference= data["defaultPreference"]	
					usertypeDetail.assignPreferences= data["assignPreferences"]			
					usertypeDetail.modifiedBy = data["modifiedBy"]
					usertypeDetail.save()
					return HttpResponse(json.dumps({"responsecode":"200","status":"Success: Edited","tId":usertypeDetail.tId}),content_type="application/json")
			if(data["action"] == "alllist"):
				userTypeObj = UserType.objects.filter(isActive=True).filter(entityId=eId)
				userTypeList = []
				for sg in userTypeObj:
					obj = {"id":sg.id,"tId":sg.tId,"entityid":sg.entityId,"typeName":sg.typeName,"description":sg.description,"defaultPreference":sg.defaultPreference,"assignPreferences":sg.assignPreferences}
					userTypeList.append(obj)
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Listed","userTypeList":userTypeList}),content_type="application/json")

			if(data["action"] == "delete"):
				usertypeDetail = UserType.objects.get(tId=data['tId'])
				usertypeDetail.isActive=False
				usertypeDetail.save()
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Deleted"}),content_type="application/json")
		else:
			return HttpResponse(json.dumps({"responsecode":"300","status":"success","msg":"No Record Exits!!!"}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({ "status" : False, "responce_code":"500","error":str(e) }), content_type="application/json")
#---------------------------------- End API's of usertypeApi ---.---------------------------------------------------#

# Create your views here.
@api_view(['POST'])
#@permission_classes((IsAuthenticated, ))
def users(request,id):
	try:
		eId=id
		data = request.data
		entityDetail = entity.objects.get(id= eId)

		if(entityDetail!=""):
			if(data["action"]=="create"):

				userDetail = Users()		
				userDetail.entityId= eId
				userDetail.userType=data["userType"]
				userDetail.name= data["name"]	
				userDetail.emailid= data["emailid"]	
				userDetail.primaryrole= data["primaryrole"]
				userDetail.save()
				
				userdetails = User()
				userdetails.first_name = data['name']
				userdetails.email = data['emailid']
				userdetails.username = userDetail.uId
				userdetails.password = data['userpass']
				userdetails.set_password(userdetails.password)  
				userdetails.save()
				
				everf = emailverify()
				everf.uId = userDetail
				everf.verifylink = id_generator(8, "6793YUIO")
				everf.save()
				
				link = "http://127.0.0.1:8000/verifyemail/"+everf.verifylink
				message ='Hello '+userDetail.name+' You Just registerd to our website so please verify your email by visting following link.'+link
				sendmail(userDetail.emailid, "Verify Email: TLRnow", message)

				return HttpResponse(json.dumps({"responsecode":"200","status":"Success: Created","msg":"Please Verify Emailid to access.","link":everf.verifylink,"uId":userDetail.uId}),content_type="application/json")	
			if(data["action"]=="edit"):
					userDetail = Users.objects.get(uId= data['uId'])
					userDetail.name= data["name"]
					userDetail.save()
					return HttpResponse(json.dumps({"responsecode":"200","status":"Success: Edited","uId":userDetail.uId}),content_type="application/json")
			if(data["action"] == "alllist"):
				userObj = Users.objects.filter(isActive=True).filter(entityId=eId)
				userList = []
				for sg in userObj:
					types = UserType.objects.get(tId= sg.userType)
					obj = {"id":sg.id,"uId":sg.uId,"name":sg.name,"typeName":types.typeName,"emailid":sg.emailid,"primaryrole":sg.primaryrole}
					userList.append(obj)
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Listed","userList":userList}),content_type="application/json")

			if(data["action"] == "delete"):
				userDetail = Users.objects.get(uId=data['uId'])
				userDetail.isActive=False
				userDetail.save()
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Deleted"}),content_type="application/json")
		else:
			return HttpResponse(json.dumps({"responsecode":"300","status":"success","msg":"No Record Exits!!!"}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({ "status" : False, "responce_code":"500","error":str(e) }), content_type="application/json")
#---------------------------------- End API's of userApi ---.---------------------------------------------------#

@api_view(['POST'])
def authenticate(request):
    try:
		# eId=id
		data = request.data
		# entityDetail = entity.objects.get(id= eId)
		userin = Users.objects.get(emailid=data["email"])
		
		# user = user = authenticate(username='admin', password='Demo@123')
		# user = User.objects.get(emailid = userin.uId, password = data["password"])
		
		if(userin != None):
			if(userin.isActive==True):
				userverf = emailverify.objects.get(uId_id = userin.uId)
				if(userverf.isVerify == True):
					parm = {"username":userin.uId,"password":data["password"]}
					user = requests.post('http://127.0.0.1:8000/api/auth/token', parm)
					jsonu = user.json()
					# payload = {'id': user.id,'email': user.email}
					# jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
					if userin.isExtrafield == False:
						redirecturl = "add extra field"
					else:
						redirecturl = "home"
					obj = {"id":userin.id,"uId":userin.uId,"entityId":userin.entityId,"name":userin.name,"typeName":userin.userType,"emailid":userin.emailid,"primaryrole":userin.primaryrole,"secondaryrole":userin.secondaryrole}
					if user.status_code == 200:
						return HttpResponse(json.dumps({"responsecode":"200","status":"Login Successful","data":obj,"token":jsonu["token"],"redirecturl":redirecturl}),content_type="application/json")
					else:
						return HttpResponse(json.dumps({"responsecode":"401","status":"Invalid Username or Password"}),content_type="application/json")
				else:
					return HttpResponse(json.dumps({"validation": "Email Not Verified please verify first then login", "status": False}), content_type="application/json")
			else:
				return HttpResponse(json.dumps({"validation": "Inactive User..!!", "status": False}), content_type="application/json")

		else:
			return HttpResponse(json.dumps({"responsecode":"400","validation": "Invalid login details..!!", "status": "User Not Available"}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"status" : "fail","msg":str(e)}), content_type = "application/json")

# Create your views here.
@api_view(['POST'])
#@permission_classes((IsAuthenticated, ))
def userExtrafield(request,id):
	# try:
		eId=id
		data = request.data
		user = Users.objects.get(uId= data["uId"])

		if(user!=""):
			if(data["action"]=="create"):

				userDetail = UsersExtrafield()		
				userDetail.uId= user
				userDetail.extrafield=data["extrafield"]
				userDetail.createdBy= data["createdBy"]
				userDetail.save()
				
				user.isExtrafield = True
				user.save()
				return HttpResponse(json.dumps({"responsecode":"200","status":"Success: Created","uId":userDetail.uId}),content_type="application/json")	
			if(data["action"]=="edit"):
					userDetail = UsersExtrafield.objects.get(uId= data['uId'])
					userDetail.extrafield= data["extrafield"]
					userDetail.modifiedBy= data["modifiedBy"]
					userDetail.save()
					return HttpResponse(json.dumps({"responsecode":"200","status":"Success: Edited","uId":userDetail.uId_id}),content_type="application/json")
			if(data["action"] == "get"):
				userObj = UsersExtrafield.objects.get(uId= data['uId'])
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Listed","uID":userObj.uId_id,"extrafield":userObj.extrafield}),content_type="application/json")

			if(data["action"] == "delete"):
				userDetail = UsersExtrafield.objects.get(uId=data['uId'])
				userDetail.isActive=False
				userDetail.save()
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Deleted"}),content_type="application/json")
		else:
			return HttpResponse(json.dumps({"responsecode":"300","status":"success","msg":"No Record Exits!!!"}),content_type="application/json")
	# except Exception as e:
		# return HttpResponse(json.dumps({ "status" : False, "responce_code":"500","error":str(e) }), content_type="application/json")
#---------------------------------- End API's of userextrafieldApi ---.---------------------------------------------------#

@api_view(['POST'])
def searchuserlistwithpagination(request,id):
    # try:
		eId=id
		data = request.data
		entityDetail = entity.objects.get(id= eId)
		
		pageNo = data['pageNo']
		entriesPerPage = data['entriesPerPage']
		name =data['name'] 
		excludePageEntries = (pageNo - 1) * entriesPerPage
		nextPageEntries = excludePageEntries + entriesPerPage
		if(name == ""):
			UserList = Users.objects.filter(entityId=eId).filter(isActive=True).order_by('-id')[excludePageEntries:nextPageEntries]
			UserListCount = Users.objects.filter(entityId=eId).filter(isActive=True).count()
						
			AllUserList = [] 
			for userin in UserList:
				# udetails = UsersExtrafield.object.get(uId = userin.uId)
				obj = {"id":userin.id,"uId":userin.uId,"entityId":userin.entityId,"name":userin.name,"typeName":userin.userType,"emailid":userin.emailid,"primaryrole":userin.primaryrole,"secondaryrole":userin.secondaryrole}   
				AllUserList.append(obj)
			return HttpResponse(json.dumps({"responce code":"200","PageNo": pageNo,"usercount": UserListCount, "userlist" : AllUserList}), content_type="application/json")
						
		elif(name != ""):
			UserList = Users.objects.filter(entityId=eId).filter(name__icontains = name,isActive=True).order_by('-id')[excludePageEntries:nextPageEntries]
					
			UserListCount = Users.objects.filter(entityId=eId).filter(name__icontains = name,isActive=True).count()
					
			AllUserList = [] 
			for userin in UserList:
				obj = {"id":userin.id,"uId":userin.uId,"entityId":userin.entityId,"name":userin.name,"typeName":userin.userType,"emailid":userin.emailid,"primaryrole":userin.primaryrole,"secondaryrole":userin.secondaryrole}   
				AllUserList.append(obj)
			return HttpResponse(json.dumps({"responce code":"200","PageNo": pageNo,"usercount": UserListCount, "userlist" : AllUserList}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({ "status" : False, "responce code":"600"}), content_type="application/json")
			
    # except Exception as e:
        # return HttpResponse(json.dumps({"status" : "fail","msg":str(e)}), content_type = "application/json")


@api_view(['GET'])
def getuserdetails(request,id,uId):
    try:
		eId=id
		type = request.data
		entityDetail = entity.objects.get(id= eId)
		userin = Users.objects.get(entityId=eId, uId= uId)
		udetails = UsersExtrafield.objects.get(uId = uId)
		if userin.isActive==True:
			obj = {"id":userin.id,"uId":userin.uId,"entityId":userin.entityId,"name":userin.name,"typeName":userin.userType,"emailid":userin.emailid,"primaryrole":userin.primaryrole,"secondaryrole":userin.secondaryrole}
			return HttpResponse(json.dumps({"responce code":"200", "userdetails" : obj,"extrafield":udetails.extrafield}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({"responce code":"401", "status" : "user not active"}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"status" : "fail","msg":str(e)}), content_type = "application/json")
		
@api_view(['POST'])
def usertypewiseuserslist(request,id):
    try:
		eId=id
		type = request.data
		entityDetail = entity.objects.get(id= eId)
		userObj = Users.objects.filter(isActive=True).filter(entityId=eId).filter(userType=type["userType"])
		userList = []
		for sg in userObj:
			types = UserType.objects.get(tId= sg.userType)
			obj = {"id":sg.id,"uId":sg.uId,"name":sg.name,"typeName":types.typeName,"emailid":sg.emailid,"primaryrole":sg.primaryrole}
			userList.append(obj)
		return HttpResponse(json.dumps({"responsecode":"200","status":"success: Listed","userList":userList}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"status" : "fail","msg":str(e)}), content_type = "application/json")
		
# Create your views here.
@api_view(['POST'])
#@permission_classes((IsAuthenticated, ))
def userFile(request,id):
	# try:
		eId=id
		data = request.data
		user = Users.objects.get(uId= data["uId"])

		if(user!=""):
			if(data["action"]=="create"):

				userf = UsersFiles()		
				userf.uId= user
				userf.filename=data["filename"]
				userf.file= data["file"]
				userf.createdBy= data["createdBy"]
				userf.save()
				return HttpResponse(json.dumps({"responsecode":"200","status":"Success: Created","fId":userf.fId}),content_type="application/json")	
			if(data["action"]=="edit"):
				userf = UsersFiles.objects.get(fId= data['fId'])
				userf.filename= data["filename"]
				userf.file= data["file"]
				userf.modifiedBy= data["modifiedBy"]
				userf.save()
				return HttpResponse(json.dumps({"responsecode":"200","status":"Success: Edited","uId":userf.uId_id}),content_type="application/json")
			if(data["action"] == "getfilebyid"):
				sg = UsersFiles.objects.get(fId= data['fId'])
				obj = {"id":sg.id,"uId":sg.uId_id,"filename":sg.filename,"fId":sg.fId,"file":sg.file.url}
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Listed","filedetails":obj}),content_type="application/json")
			if(data["action"] == "getfilesbyuser"):
				userObj = UsersFiles.objects.filter(uId= data['uId'])
				fobj=[]
				for sg in userObj:
					obj = {"id":sg.id,"uId":sg.uId_id,"filename":sg.filename,"file":sg.file.url,"fId":sg.fId}
					fobj.append(obj)
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Listed","filedetails":fobj}),content_type="application/json")

			if(data["action"] == "delete"):
				userDetail = UsersFiles.objects.get(uId=data['fId'])
				userDetail.isActive=False
				userDetail.save()
				return HttpResponse(json.dumps({"responsecode":"200","status":"success: Deleted"}),content_type="application/json")
		else:
			return HttpResponse(json.dumps({"responsecode":"300","status":"success","msg":"No Record Exits!!!"}),content_type="application/json")
	# except Exception as e:
		# return HttpResponse(json.dumps({ "status" : False, "responce_code":"500","error":str(e) }), content_type="application/json")
#---------------------------------- End API's of userApi ---.---------------------------------------------------#

@api_view(['POST']) 
def forgotpassword(request, id):
	data = request.data
	email = data['email']
	userdetail = Users.objects.get(emailid = email, isActive = True)
	if(userdetail != None):
		userdata = User.objects.get(username = userdetail.uId)
		newlink= id_generator(8, "6793YUIO")
		# userdata.password = newpass
		# userdata.set_password(userdata.password)
		# userdata.save()
		res = resetpassword()
		res.uId = userdetail
		res.resetlink = newlink
		res.save()
		
		subject='Password Reset'
		link = "http://127.0.0.1:8000/resetpassword/"+newlink
		message ='Hello '+userdetail.name+' You Just Requested for Your password reset password plz visit following link to reset password '+link
		sendmail(userdata.email, subject, message)
		
		return HttpResponse(json.dumps({"status" : True, "statuscode" : "200", "msg" : "Plz Check you email inbox for new password."}), content_type = "application/json")
		
	else:
		return HttpResponse(json.dumps({"status" : True, "statuscode" : "102", "msg" : "User Not Present"}), content_type = "application/json")
		
@api_view(['POST'])
def ResetPassword(request,lId):
		data = request.data
		resetdetails = resetpassword.objects.get(resetlink= lId)
		if(resetdetails.isActive == True):
			users = Users.objects.get(uId = resetdetails.uId_id)
			userdata = User.objects.get(username = resetdetails.uId_id)
			userdata.password = data["newpass"]
			userdata.set_password(userdata.password)
			userdata.save()
			
			resetdetails.isActive = False
			resetdetails.save()
			
			message ='Hello '+users.name+' You Just changed your password successfuly'
			sendmail(users.emailid, "Password Changed", message)
			return HttpResponse(json.dumps({"status" : True, "statuscode" : "200", "msg" : "your password successfuly changed"}), content_type = "application/json")
		else:
			return HttpResponse(json.dumps({"responsecode":"102","status":"Verification Link Expired"}),content_type="application/json")
			
@api_view(['GET'])
def verifyemail(request,vId):
		verifydetails = emailverify.objects.get(verifylink= vId)
		if(verifydetails.isActive == True):
			users = Users.objects.get(uId = verifydetails.uId_id)
			
			verifydetails.isActive = False
			verifydetails.isVerify = True
			verifydetails.save()
			
			message ='Hello '+users.name+' You Just Verified your email successfuly'
			sendmail(users.emailid, "Email Verification: TLRnow", message)
			return HttpResponse(json.dumps({"status" : True, "statuscode" : "200", "msg" : "your password successfuly changed"}), content_type = "application/json")
		else:
			return HttpResponse(json.dumps({"responsecode":"102","status":"Verification Link Expired"}),content_type="application/json")