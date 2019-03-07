#!/usr/bin/env python3
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import wx
from guiUtils import *
from utils import *




class NotifyHandler(FTPHandler):

	def bindGui(self, gui):
		self.gui=gui
		self.trayIcon=gui.trayIcon
	
	def	appendOutput(self,s):
		count=self.gui.listCtrlStatus.GetItemCount()
		wx.CallAfter(self.gui.listCtrlStatus.InsertItem,count,s)
		wx.CallAfter(self.gui.listCtrlStatus.Focus, count)
	
	def on_connect(self):
		print("User connected.")
		self.appendOutput('('+getDatetime()+') '+_("User connected."))

	def on_disconnect(self):
		print("User disconnected.")
		self.appendOutput('('+getDatetime()+') '+_("User disconnected."))

	def on_login(self, username):
		self.appendOutput('('+getDatetime()+') '+_("User %s has log in." % username))

	def on_logout(self, username):
		self.appendOutput('('+getDatetime()+') '+_("User %s has log out." % username))

	def on_file_sent(self, file):
		# do something when a file has been sent
		self.appendOutput('('+getDatetime()+') '+_("File %s has has been sent." % str(file)))

	def on_file_received(self, file):
		# do something when a file has been received
		self.appendOutput('('+getDatetime()+') '+_("File %s has has been received." % str(file)))

	def on_incomplete_file_sent(self, file):
		# do something when a file is partially sent
		self.appendOutput('('+getDatetime()+') '+_("File %s has has been **partially sent** ." % str(file)))

	def on_incomplete_file_received(self, file):
		# remove partially uploaded files
		self.appendOutput('('+getDatetime()+') '+_("File %s has has been **partially received** ." % str(file)))
		import os
		os.remove(file)







class TFtpServer():
	
	
	def __init__(self, gui):
		self.gui=gui
		self.trayIcon=gui.trayIcon
		self.started=False	
	
	def generalConfig(self):
		self.prefs = configparser.ConfigParser()
		self.prefs.read(getConfGeneralFilePath())
	
	def loadUsers(self):
		self.configUsers = configparser.ConfigParser()
		self.configUsers.read(getConfUsersFilePath())
		self.usernames=self.configUsers.sections()
		for u in self.usernames:
			username=u
			password=self.configUsers[u]['password']
			root_folder=self.configUsers[u]['root_folder']
			if (self.configUsers[u]['readonly']=='True'):
				perm='elr'
			else:
				perm='elradfmwMT'
			self.authorizer.add_user(username, password, root_folder, perm)			
		
	def start(self):
		try:
			self.authorizer = DummyAuthorizer()
			
			#Anonymous user
			self.generalConfig()
			if (self.prefs['anonymous']['enable']=='True'):
				if (self.prefs['anonymous']['readonly']=='False'):
					self.authorizer.add_anonymous(self.prefs['anonymous']['root_folder'], perm='elradfmwMT')
				else:
					self.authorizer.add_anonymous(self.prefs['anonymous']['root_folder'], perm='elr')
			
			#Users
			confUsersFile=getConfUsersFilePath()
			if (os.path.isfile(confUsersFile)):
				self.loadUsers()
				
			self.handler = NotifyHandler
			self.handler.bindGui(self.handler,self.gui)
			self.handler.authorizer = self.authorizer
			self.handler.passive_ports=range(60000, 65535)
			
			#internet connections
			#self.handler.masquerade_address=''
			self.handler.permit_foreign_addresses=True

			self.server = FTPServer(("0.0.0.0", self.prefs['general']['ftp_port']), self.handler)
			self.started=True
			wx.CallAfter(self.gui.serverStarted)
			self.server.serve_forever()
			
		except OSError as e:
			print("Os Error: %s" % e)
			self.started=False
			wx.CallAfter(self.gui.serverFailed, e)

		except ValueError as e:
			print("Value Error : %s" % e)
			self.started=False	
			wx.CallAfter(self.gui.serverFailed, e)
		
		'''except Exception as e:
			print("Error : %s" % e)
			self.started=False
			wx.CallAfter(Warn, self.gui.mainFrame, str(e))	
		'''
	def stop(self):
		self.server.close_all()
		self.started=False
		wx.CallAfter(self.gui.serverNormal)
		del self

#Gettex
import locale, gettext
try:
	current_locale, encoding = locale.getdefaultlocale()
	locale_path = 'locale'
	language = gettext.translation ('pobshare', locale_path, [current_locale] )
	language.install()
	
except:
	_ = gettext.gettext
