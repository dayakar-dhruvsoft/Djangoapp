from django.db import models

# Create your models here.
class SF_Details(models.Model):
	Salesforce_Edition=models.CharField(max_length=30)
	Salesforce_Org_ID = models.CharField(max_length=50,primary_key=True)
	Salesforce_Org_Name = models.CharField(max_length=60)
	Connected_by_User_Name=models.CharField(max_length=70)
	Access_Token=models.CharField(max_length=130)
	Refresh_Token=models.CharField(max_length=100)