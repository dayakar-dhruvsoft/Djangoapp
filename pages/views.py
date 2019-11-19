from django.shortcuts import render
from django.http import HttpResponse,HttpResponseServerError,Http404,HttpResponseNotFound
from django.shortcuts import redirect
from urllib import request
from django.core.exceptions import SuspiciousOperation
import logging
import requests
from .models import SF_Details
from pages.config import consumer_key, consumer_secret,authorize_url,redirect_uri, access_token_url
def HomePageView(request):
    return render(request,'home.html')
def login(request):
   url ="{}?response_type=code&client_id={}&redirect_uri={}" .format(authorize_url, consumer_key, redirect_uri)
   return redirect(url)
def callback(request):
    code = request.GET.get('code')
    #value=request.GET.get('callback')
    print(code)
    params = {  
                'grant_type': 'authorization_code',
                'client_id' : consumer_key,
                'client_secret' : consumer_secret,
                'redirect_uri':redirect_uri,
                'code':code
    }
    req_token = requests.post(access_token_url, params=params)
    if req_token.status_code!=200:
        return HttpResponseServerError("Invalid Request:Unable to fetch the Salesforce Authorization information.")
    try:
   		response = req_token.json()
   		#if 'access_token' in response and 'refresh_token' in response and 'instance_url' in response:
   		access_token=response.get('access_token',None)
   		refresh_token=response.get('refresh_token',None)
   		instance_url=response.get('instance_url',None)
   		print(access_token)
   		#else:
   		#	raise ("<b>Unable to fetch the Access Token in the response.</b>")
   		url=instance_url+"/services/oauth2/userinfo"
   		req_name = requests.get(url, headers = {"Authorization":"Bearer " + access_token})
   		req_username=req_name.json()
   		connected_by_user_name=req_username.get('name')
   		urls=instance_url+'/services/data/v20.0/query?q=SELECT+Name,id,OrganizationType+from+Organization'
   		req_orginfo = requests.get(urls, headers = {"Authorization":"Bearer " + access_token})
   		req_info=req_orginfo.json()
   		for orgrec in req_info['records']:
   			Salesforce_edition=(orgrec['OrganizationType'])
   			Salesforce_org_id=(orgrec['Id'])
   			Salesforce_org_name=(orgrec['Name'])
    except Exception as e:
       logging.error(e)
       if(req_name.status_code!=200 or req_orginfo.status_code!=200):
        	return HttpResponseNotFound("Error: The requested page was not found for fetching Salesforce information.")
       else:
       		print("Sorry, Unable to fetch the Salesforce information.")
       		return "Invalid Request: Missed the parameters while fetching Salesforce org information"
    Salesforce_details={
            'Salesforce Edition: ':Salesforce_edition,
            'Salesforce Org ID: ':Salesforce_org_id,
            'Salesforce Org Name: ':Salesforce_org_name,
            'Connected by User Name: ':connected_by_user_name,
            'Access Token: ':access_token,
            'Refresh Token: ':refresh_token   
    }
    update_data=SF_Details.objects.filter(Salesforce_Org_ID=Salesforce_org_id)
    if update_data:
    	 update_data.update(Salesforce_Edition=Salesforce_edition)
    	 update_data.update(Salesforce_Org_Name=Salesforce_org_name)
    	 update_data.update(Connected_by_User_Name=connected_by_user_name)
    	 update_data.update(Access_Token=access_token)
    	 update_data.update(Refresh_Token=refresh_token)
    else:
   		exist_data=SF_Details.objects.create(Salesforce_Edition=Salesforce_edition,Salesforce_Org_ID=Salesforce_org_id,Salesforce_Org_Name=Salesforce_org_name,Connected_by_User_Name=connected_by_user_name,Access_Token=access_token,Refresh_Token=refresh_token)
    return render(request,'a.html',{'result':Salesforce_details})