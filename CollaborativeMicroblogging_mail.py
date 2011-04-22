# CollaborativeMicroblogging_mail.py
# Its microblogging interfaced with xmpp. Useful for storming sessions.
# Currently just enables us to post twitter updates using xmpp and get replies over mail

# Author       - Harshad Joshi
# Date         - 22 April 2011
# eMAIL        - firewalrus [AT] gmail {DOT} com  

# Requirements - Twitter Account
#	       - XMPP chat server (openfire) / GTalk
#              - Python 2.5 with xmpppy and tweepy library.
#
# Features     - Unicode enabled
#              - Sends Mentions on mail   
#
# ToDo         - Add some mechanism to send replies on xmpp..didnt do it becasue tweepy provided extremely skimpy documentation
# 	       - Add some more scalability to the bot, ie instead of hardcoding the blog/user/passwd within the program, 
#              - should ask for it once and store it in the backend.
#              - This app will make use of sms and mail interface in the next version... 
#              - Add sms updates    
#              - Enable reading of public timeline, user timeline, DM etc..


#This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301, USA.




import sys
import xmpp
import codecs
import tweepy
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64



xmpp_user='user@gmail.com'
xmpp_passwd='passw'
xmpp_server='gmail.com or xmpp server '

# This example is specifiacally meant to use gmail as smtp server..change the settings(port number, address etc) if you have got a dedicated email id
user='you@gmail.com'
passwd='gmailpasswd'
server='gmail.com'


#get this from twitter...you can find complete information and howto from this site - http://jeffmiller.github.com/2010/05/31/twitter-from-the-command-line-in-python-using-oauth
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

ACCESS_KEY = ''
ACCESS_SECRET = ''



class CollaborativeMicroblogging:
	def message_handler(connect_object,message_node):
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
                
		mymentions = api.mentions() 		
		
		incoming1=str(unicode(message_node.getBody()).encode('utf-8'))
		incoming2=str(message_node.getFrom().getStripped())
		
		c3=incoming2.replace("@"," [at] ")
		c4=c3.replace("."," [dot] ")		
		b = incoming1.split()
		if (b[0] == 'mentions'):
			gmailUser = user
			gmailPassword = passwd
			recipient = 'wheredoyouwant@email.com'
			
                        			
			for tweet in mymentions:
				d = tweet.text+" >>  "+str(tweet.user.screen_name)
				msg = MIMEMultipart()
				msg['From'] = gmailUser
				msg['To'] = recipient
				msg['Subject'] = incoming2+" has sent a reply message to you"				
				mailServer = smtplib.SMTP('smtp.gmail.com', 587)
				mailServer.ehlo()
				mailServer.starttls()
				mailServer.ehlo()
				mailServer.login(gmailUser, gmailPassword)
				mailServer.sendmail(gmailUser, recipient, d)
				mailServer.close()  
		else:
			api.update_status(incoming1)
                	#dir(api)

		            
	
		connect_object.send(xmpp.Message(message_node.getFrom(),("Posted your message on Twitter "+incoming1)))				
	
		
	jid=xmpp.JID(user)
	connection=xmpp.Client(server)
	connection.connect()
	result=connection.auth(jid.getNode(),passwd)
	connection.RegisterHandler('message',message_handler,"")
	connection.sendInitPresence()
        press = xmpp.Presence()
        press.setStatus("Hi from Collaborative Microblogging App")
        connection.send(press)

	while (1):
		connection.Process(1)


a=CollaborativeMicroblogging()
a

	



