# * coding: utf-8 *
# This programs runs on a localhost xmpp server and logs all the messages sent to it on identi.ca
# Its a sort of federated microblogging with a database backend. 
# Author       - Harshad Joshi
# Date         - 24 April 2011
#
# Requirements - ident.ca or statusnet account
#	       - XMPP chat server (openfire)
#              - Python 2.5 with xmpp and xml-rpc library.
#
# Features     - Unicode enabled
#
# ToDo         - Add some mechanism to receive replies over xmpp and not mail
#
# Shouts       - Many thanks to @bavatar for sharing initial code from line 38-42 and 53-57

# All legal or license stuff...in one single line - dont steal code

# This program is free software; you can redistribute it and/or modify
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

import time
import xmpp
import codecs
import json, urllib2
from urllib import urlencode


user='you@gmail.com'
passwd='gmailpasswd'
server='gmail.com'



# some stuff to identify yourself against the server
# and the base API path
identiuser = "your_identi.ca_username"
pwd = "your_identi.ca_passwd"
apibase = "https://identi.ca/api"

pwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
pwd_mgr.add_password(None, apibase, identiuser, pwd)
handler = urllib2.HTTPBasicAuthHandler(pwd_mgr)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)



class IdentiCa:
	def message_handler(connect_object,message_node):
		command1=str(unicode(message_node.getBody()).encode('utf-8'))
		command2=str(message_node.getFrom().getStripped())
		c3=command2.replace("@"," [at] ")
		c4=c3.replace("."," [dot] ")		
		# now define a message
		msg = command1
		# url encode it nicely and set your own client name – no links in source!
		themsg = urlencode({'status':msg,'source':'CollaborativeMicroblogging'})
		# and send the notice
		urllib2.urlopen(apibase+'/statuses/update.json?s', themsg)

		            
	
		connect_object.send(xmpp.Message(message_node.getFrom(),("Posted your message on Twitter "+command1)))				
	
		
	jid=xmpp.JID(user)
	connection=xmpp.Client(server)
	connection.connect()
	result=connection.auth(jid.getNode(),passwd)
	connection.RegisterHandler('message',message_handler,"")
	connection.sendInitPresence()
        press = xmpp.Presence()
        press.setStatus("Hi from Federated Microblogging App")
        connection.send(press)

	while (1):
		connection.Process(1)

a=IdentiCa()
a

	



