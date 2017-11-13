from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-

class HostList(models.Model):
    ip = models.CharField(max_length=20)
    hostname = models.CharField(max_length=30)
    status = models.CharField(max_length=10)
    remark = models.TextField(max_length=50, blank=True)

    def __str__(self):
        return '%s  %s  %s' %(self.ip, self.hostname, self.status )
	
    class Mete:
    	db_table='HostList'



class User(models.Model):
	username=models.CharField(max_length=20)
	password=models.CharField(max_length=50)
	status=models.CharField(max_length=10, default='active')

	def __str__(self):
		return '%s' %(self.username)

	class Mete:
		db_table='User'
