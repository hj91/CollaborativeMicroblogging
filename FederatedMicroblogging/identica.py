#!/usr/bin/env python
# * coding: utf-8 *
# (c) Harshad Joshi, 18 Jul 2011
# Little refactoring done
# ToDo 
# Give it some error and exception handling and make it as versatile as it can become.

import json, urllib2
from urllib import urlencode
import sys,feedparser

def url(a):
	n=urllib2.urlopen(a)
	b=feedparser.parse(n)
	for i in range(len(b.entries)):
	       	print b.entries[i].title
	del(n)
	del(b)
	
def url2(a):
	n=urllib2.urlopen(a)
	b=feedparser.parse(n)
	for entry in b.entries:
		print entry.title, entry.id
	del(n)
	del(b)

class IdentiCa:
	def __init__(self,user,pwd,apibase):
		self.user = user
		self.pwd = pwd
		self.apibase = apibase
		

	def post(self,msg):
	# connection magic
		pwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		pwd_mgr.add_password(None, self.apibase, self.user, self.pwd)
		handler = urllib2.HTTPBasicAuthHandler(pwd_mgr)
		opener = urllib2.build_opener(handler)
		urllib2.install_opener(opener)

	# now define a message
		
		if (msg.lower() == 'exit'):
			sys.exit(0)
		else:
			if (msg.lower() == 'mentions'):
				url("http://identi.ca/index.php/api/statuses/mentions/"+self.user+".rss")
			else:
				if (msg.lower() == 'home'):
					url("http://identi.ca/api/statuses/friends_timeline/"+self.user+".rss")
				else:
					if (msg.lower() == 'friends'):
						url2('http://identi.ca/api/statusnet/app/subscriptions/32987.atom')
						
						v=raw_input('Enter the id of friend you want to see updates of >> ')
						url("http://identi.ca/api/statuses/user_timeline/"+v+".atom")
						
		
					else:
						if (msg.lower() == 'status'):
							e=raw_input("Enter your status >> ")				
							# url encode it nicely and set your own client name â€“ no links in source!
							themsg = urlencode({'status':e,'source':'CollaborativeMicroblogging'})
							# and send the notice
							urllib2.urlopen(self.apibase+'/statuses/update.json?s', themsg)


m=IdentiCa(user = "hj91",pwd = "yourpasswd ",apibase = "https://identi.ca/api")
while(1):
	c=raw_input ("Enter somthing >> ")
	m.post(c)
	