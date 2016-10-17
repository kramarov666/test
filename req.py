#!/usr/bin/python

import urllib
import re
import requests
import datetime
import time
import pytz 
import os 
url="https://192.168.122.20"
path="xml"
headers = {'content-type': 'text/xml'}
report=open('report.txt','w+')
for name in os.listdir(path):
        print path + "/" + name
        fullpath = path + "/" + name   
      	file = open(fullpath, 'r+')
	#headers = {'content-type': 'application/soap+xml'}
	body = file.read()
	#print body
	#exttaskid
	#parsing input xml
	taskid_regex="<exttaskid>(.+?)</exttaskid>"
	taskid_regex=re.compile(taskid_regex)
	taskid_regex=re.findall(taskid_regex,body)	
	taskid_regex=''.join(taskid_regex)
	taskid_regex=int(taskid_regex)
	taskid_regex=taskid_regex + 1

	#taskid wholestring
	i1taskid_regex_wholestring="(<exttaskid>.+?</exttaskid>)"
	taskid_pattern_wholestring=re.compile(taskid_regex_wholestring)
	#taskid_str_wholestring=''.join(taskid_pattern_wholestring)
	taskid_pure_wholestring=re.findall(taskid_pattern_wholestring,body)
	taskid_pure_wholestring=''.join(taskid_pure_wholestring)
	body=body.replace(taskid_pure_wholestring,"<exttaskid>" + str(taskid_regex) + "</exttaskid>")
	file.seek(0)
        file.truncate()
	file.write(body)
	#response = requests.post(url,data=body,headers=headers,verify='ukrgaz_prod.pem')
	#date insertion	
	requestdate_regex="(<requestdate>.+?</requestdate>)"	
	exttaskdate_regex="(<exttaskdate>.+?</exttaskdate>)"
	taskuserdate_regex="(<taskuserdate>.+?</taskuserdate>)"
	
	requestdate_regex=re.compile(requestdate_regex)
	requestdate_regex=re.findall(requestdate_regex,body)
	requestdate_regex=''.join(requestdate_regex)

 	exttaskdate_regex=re.compile(exttaskdate_regex)
	exttaskdate_regex=re.findall(exttaskdate_regex,body)
	exttaskdate_regex=''.join(exttaskdate_regex)

	taskuserdate_regex=re.compile(taskuserdate_regex)
	taskuserdate_regex=re.findall(taskuserdate_regex,body)
	taskuserdate_regex=''.join(taskuserdate_regex)
	
	body=body.replace(requestdate_regex,"<requestdate>" + datetime.datetime.now(pytz.timezone('Europe/Kiev')).isoformat() + "</requestdate>")
	body=body.replace(exttaskdate_regex,"<exttaskdate>" + datetime.datetime.now(pytz.timezone('Europe/Kiev')).isoformat() + "</exttaskdate>")
	body=body.replace(taskuserdate_regex,"<taskuserdate>" + datetime.datetime.now(pytz.timezone('Europe/Kiev')).isoformat() + "</taskuserdate>")	
	#print body
	#taskstatus_regex="<taskstatus>(.+?)</taskstatus>"
	#taskstatus_regex=re.compile(taskstatus_regex)
        #htmlfile=urllib.urlopen(url)
	
	#htmltext=response.content
	#taskstatus_regex=re.findall(taskstatus_regex.htmltext)
	def ServCon ():
		"""
		#change to urlcoonnect
		TempFile=open('success.txt', 'r')
		#print body
		TempFile = TempFile.read()
		print TempFile
		#
		"""
		response = requests.post(url,data=body,headers=headers,verify='ukrgaz_prod.pem')
		global taskstatus_regex
		taskstatus_regex="<taskstatus>(.+?)</taskstatus>"
		taskstatus_regex=re.compile(taskstatus_regex)
       		taskstatus_regex=re.findall(taskstatus_regex,response.content)
		taskstatus_regex=''.join(taskstatus_regex)	
		
		print taskstatus_regex + "  -  " + name
		report_string=taskstatus_regex + "  -  " + name	
		
		report.write(datetime.datetime.now(pytz.timezone('Europe/Kiev')).isoformat()+ " " + report_string + '\n')
	count=1
	ServCon ()
	while taskstatus_regex == 'CREATED':
		time.sleep(1)		
		count=count+1
		#print count
		if count == 5:
			print "more than " +str(count)+ " iterables, i've broken this loop"				
			break		
		ServCon()
	while taskstatus_regex == 'PROCESSED':
		time.sleep(1)			
		count=count+1
		#print count
		if count == 5:
			print "more than " +str(count)+ " iterables, i've broken this loop"				
			break			
		ServCon()
	



#print titles


#print datetime.datetime.now(pytz.timezone('Europe/Kiev')).isoformat()
#print response.content

	
	file.close()
report.close()
report=open('report.txt','r')
print report.read()
report.close()
