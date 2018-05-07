"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<id>[\w-]+)/usertypeapi/$',views.usertype,name="usertypeapi"),
	url(r'^(?P<id>[\w-]+)/users/$',views.users,name="users"),
	url(r'^(?P<id>[\w-]+)/userextrafield/$',views.userExtrafield,name="userExtrafield"),
	url(r'^authenticate/$',views.authenticate,name="authenticate"),
	url(r'^(?P<id>[\w-]+)/usertypewiseuserlist/$',views.usertypewiseuserslist,name="usertypewiseuserslist"),
	url(r'^(?P<id>[\w-]+)/getuserdetails/(?P<uId>[\w-]+)$',views.getuserdetails,name="getuserdetails"),
	url(r'^(?P<id>[\w-]+)/searchuserlistwithpagination/$',views.searchuserlistwithpagination,name="searchuserlistwithpagination"),
	url(r'^(?P<id>[\w-]+)/userfiles/$',views.userFile,name="userFile"),
	url(r'^(?P<id>[\w-]+)/forgotpassword/$',views.forgotpassword,name="forgotpassword"),
	url(r'^resetpassword/(?P<lId>[\w-]+)$',views.ResetPassword,name="ResetPassword"),
	url(r'^verifyemail/(?P<vId>[\w-]+)$',views.verifyemail,name="verifyemail"),
]