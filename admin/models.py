from django.db import models

# User Model
class User(models.Model):
	username = models.CharField(max_length=32);
	password = models.CharField(max_length=32);
	nick = models.CharField(max_length=32, null=True);
	mail = models.EmailField(max_length=64, null=True);
	jointime = models.DateTimeField();
	lastlogintime = models.DateTimeField(null=True);
	status = models.BooleanField(default=True);

# Role Model
class Role(models.Model):
	name = models.CharField(max_length=32);
	pid = models.IntegerField(default=0);
	orderdisplay = models.IntegerField(max_length=5, default=0);
	status = models.BooleanField(default=True);

# SystemFunction Model
class SystemFunction(models.Model):
    name = models.CharField(max_length=64);
    url = models.CharField(max_length=64, null=True);
    accessurl = models.TextField(null=True);
    pid = models.IntegerField(default=0);
    orderdisplay = models.IntegerField(max_length=5, default=0);
    ismenu = models.BooleanField(default=False);
    icon = models.CharField(max_length=64, null=True);
    status = models.BooleanField(default=True);

# UserRole Model
class UserRole(models.Model):
	user = models.ForeignKey(User);
	role = models.ForeignKey(Role);	

# Access Model
class SystemFunctionRole(models.Model):
	role = models.ForeignKey(Role);		
	systemfunction = models.ForeignKey(SystemFunction);