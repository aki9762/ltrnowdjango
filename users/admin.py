# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import UserType, Users, emailverify, resetpassword
from django.contrib import admin

# Register your models here.
admin.site.register(UserType)
admin.site.register(Users)
admin.site.register(emailverify)
admin.site.register(resetpassword)