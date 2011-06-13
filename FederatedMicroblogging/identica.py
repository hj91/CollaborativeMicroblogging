#!/usr/bin/env python
# * coding: utf-8 *
# (c) Harshad Joshi, 2011
# http://identi.ca/hj91

import json, urllib2
from urllib import urlencode
import sys,feedparser


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
				a=urllib2.urlopen("http://identi.ca/index.php/api/statuses/mentions/hj91.rss")
				b=feedparser.parse(a)
				for i in range(len(b.entries)):
	        			print b.entries[i].title
				del(a)
				del(b)
			else:
				if (msg.lower() == 'friends'):
					a=urllib2.urlopen('http://identi.ca/api/statusnet/app/subscriptions/32987.atom')
					b=feedparser.parse(a)
					c=[]
					print 'The list of your friends is'				
					for entry in b.entries:
						print entry.title, entry.id

					v=raw_input('Enter the id of friend you want to see updates of ')
					t=urllib2.urlopen("http://identi.ca/api/statuses/user_timeline/"+v+".atom")
					l=feedparser.parse(t)
					for y in l.entries:
						print y.title
	
				else:
					if (msg.lower() == 'status'):
						e=raw_input("Enter your status")				
						# url encode it nicely and set your own client name – no links in source!
						themsg = urlencode({'status':e,'source':'CollaborativeMicroblogging'})
						# and send the notice
						urllib2.urlopen(self.apibase+'/statuses/update.json?s', themsg)

	

m=IdentiCa(user = "hj91",pwd = "yourpasswd ",apibase = "https://identi.ca/api")
while(1):
	c=raw_input("Enter mentions, friends or status >> ")
	m.post(c)