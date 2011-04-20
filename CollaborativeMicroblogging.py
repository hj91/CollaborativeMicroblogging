# CollaborativeMicroblogging.py
# Its microblogging interfaced with xmpp. Useful for storming sessions.
# Author       - Harshad Joshi
# Date         - 20 April 2011
# eMAIL        - firewalrus [AT] gmail {DOT} com  
#
# Requirements - Twitter Account
#	       - XMPP chat server (openfire) / GTalk
#              - Python 2.5 with xmpppy and tweepy library.
#
# Features     - Unicode enabled
#
# ToDo         - Add some mechanism to send replies on xmpp..didnt do it becasue tweepy provided extremely skimpy documentation
# 	       - Add some more scalability to the bot, ie instead of hardcoding the blog/user/passwd within the program, 
#              - should ask for it once and store it in the backend.
#              - This app will make use of sms and mail interface in the next version... 




import sys
import xmpp
import codecs
import tweepy


user='user@gmail.com'
passwd='passw'
server='gmail.com or xmpp server '

#get this from twitter...you can find complete information and howto from this site - http://jeffmiller.github.com/2010/05/31/twitter-from-the-command-line-in-python-using-oauth
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

ACCESS_KEY = ''
ACCESS_SECRET = ''




class CollaborativeMicroblogging:
	def message_handler(connect_object,message_node):
		command1=str(unicode(message_node.getBody()).encode('utf-8'))
		command2=str(message_node.getFrom().getStripped())
		c3=command2.replace("@"," [at] ") 
		c4=c3.replace("."," [dot] ")		
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		api.update_status(command1)
                           
	
		connect_object.send(xmpp.Message(message_node.getFrom(),("Posted your message on Twitter "+command1)))				
	
		
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

	



