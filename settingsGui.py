#!/usr/bin/env python3
import wx
from wx import xrc
import os
from utils import *
from editUser import *
from guiUtils import *


#Gettex
import locale, gettext
try:
	current_locale, encoding = locale.getdefaultlocale()
	locale_path = 'locale'
	language = gettext.translation ('pobshare', locale_path, [current_locale] )
	language.install()
	
except:
	_ = gettext.gettext

class formSettings():
	
		
	def __init__(self, frame):
		
		#Settings Window
		self.res = xrc.XmlResource(os.path.join('gui','main.xrc'))
		self.frmSettings = self.res.LoadDialog(frame, 'frmSettings')
		
		#Widgets
		self.listUsers = xrc.XRCCTRL(self.frmSettings, 'listUsers')
		self.chkEnableAtStartup=xrc.XRCCTRL(self.frmSettings, 'chkEnableAtStartup')
		self.chkRunServerAtStart=xrc.XRCCTRL(self.frmSettings, 'chkRunServerAtStart')
		self.spinCtrlServerPort=xrc.XRCCTRL(self.frmSettings, 'spinCtrlServerPort')
		self.chkEnableAnonymous=xrc.XRCCTRL(self.frmSettings, 'chkEnableAnonymous')
		self.chkReadOnlyAnonymous=xrc.XRCCTRL(self.frmSettings, 'chkReadOnlyAnonymous')
		self.dirPckrAnonymousRoot=xrc.XRCCTRL(self.frmSettings, 'dirPckrAnonymousRoot')
		self.btCancel=xrc.XRCCTRL(self.frmSettings, 'btCancel')
		self.btSave=xrc.XRCCTRL(self.frmSettings, 'btSave')
		self.btResetConf=xrc.XRCCTRL(self.frmSettings, 'btResetConf')
		
		#Users button
		self.btNewUser=xrc.XRCCTRL(self.frmSettings, 'btNewUser')
		self.btEditUser=xrc.XRCCTRL(self.frmSettings, 'btEditUser')
		self.btDelUser=xrc.XRCCTRL(self.frmSettings, 'btDelUser')
		
		
		#Bind widgets
		self.btSave.Bind(wx.EVT_BUTTON, self.saveConfig)
		self.btCancel.Bind(wx.EVT_BUTTON, self.Close)
		self.btNewUser.Bind(wx.EVT_BUTTON, self.addUser)
		self.btEditUser.Bind(wx.EVT_BUTTON, self.editUser)
		self.btDelUser.Bind(wx.EVT_BUTTON, self.delUser)
		self.listUsers.Bind(wx.EVT_LIST_ITEM_SELECTED,self.userSelected)
		self.btResetConf.Bind(wx.EVT_BUTTON, self.resetConfiguration)
		
		
		#init
		self.listUsers.AppendColumn(_('Username'))
		self.listUsers.AppendColumn(_('Root Folder'))
		self.listUsers.AppendColumn(_('Read Only'))
		
		
		confFile=getConfGeneralFilePath()
		if (os.path.isfile(confFile)):
			self.loadConfig()
		
		confUsersFile=getConfUsersFilePath()
		if (os.path.isfile(confUsersFile)):
			self.loadUsers()
	
	
			
	
	def initConfig(self):
		self.config = configparser.ConfigParser()
		self.config.read(getConfGeneralFilePath())
	
	def loadConfig(self):
		self.initConfig()
		if (self.config['general']['enable_at_startup']=='True'):
			self.chkEnableAtStartup.SetValue(True)
		else:
			self.chkEnableAtStartup.SetValue(False)	
		
		if (self.config['general']['run_server_at_start']=='True'):
			self.chkRunServerAtStart.SetValue(True)
		else:
			self.chkRunServerAtStart.SetValue(False)
		
		if (self.config['general']['ftp_port']!=''):
			self.spinCtrlServerPort.SetValue(self.config['general']['ftp_port'])	
		
		if (self.config['anonymous']['enable']=='True'):
			self.chkEnableAnonymous.SetValue(True)
		else:
			self.chkEnableAnonymous.SetValue(False)	
		
		if (self.config['anonymous']['readonly']=='True'):
			self.chkReadOnlyAnonymous.SetValue(True)
		else:
			self.chkReadOnlyAnonymous.SetValue(False)				
	
		if (self.config['anonymous']['root_folder']!=''):
			self.dirPckrAnonymousRoot.SetPath(self.config['anonymous']['root_folder'])
		
	
	
	def loadUsers(self):
		try:
			self.listUsers.DeleteAllItems()
			self.configUsers = configparser.ConfigParser()
			self.configUsers.read(getConfUsersFilePath())
			self.usernames=self.configUsers.sections()
			for u in self.usernames:
				username=u
				password=self.configUsers[u]['password']
				root_folder=self.configUsers[u]['root_folder']
				if (self.configUsers[u]['readonly']=='True'):
					ro='yes'
				else:
					ro='no'
				
				self.listUsers.Append([username,root_folder,ro])
		except KeyError as e:
			Warn(self.frmSettings, _("Error on users file"), caption = 'Warning!')
				
				
	def Close(self,evt):
		self.frmSettings.Close()
	
	def saveConfig(self, evt):
		if(self.chkEnableAtStartup.GetValue()==True):
			self.config['general']['enable_at_startup']='True'
			EnableAutorunAtLogin()
		else:
			self.config['general']['enable_at_startup']='False'
			DisableAutorunAtLogin()
			
		if(self.chkRunServerAtStart.GetValue()==True):
			self.config['general']['run_server_at_start']='True'
		else:
			self.config['general']['run_server_at_start']='False'
		
		if(self.spinCtrlServerPort.GetValue()>10):
			self.config['general']['ftp_port']=	str(self.spinCtrlServerPort.GetValue())
		
		if(self.chkEnableAnonymous.GetValue()==True):
			self.config['anonymous']['enable']='True'
		else:
			self.config['anonymous']['enable']='False'			
		
		if(self.chkReadOnlyAnonymous.GetValue()==True):
			self.config['anonymous']['readonly']='True'
		else:
			self.config['anonymous']['readonly']='False'
			
		if (os.path.isdir(self.dirPckrAnonymousRoot.GetPath())):
			self.config['anonymous']['root_folder']=self.dirPckrAnonymousRoot.GetPath()
		else:
			Warn(self.frmSettings, _("The folder must exist!"), caption = 'Warning!')
			return	
		
		with open(getConfGeneralFilePath(), 'w') as configfile:
			self.config.write(configfile)
		
		self.frmSettings.Close()
		
	def Show(self):	
		self.frmSettings.ShowModal()

	def addUser(self, evt):
		winUser= formEditUser(self)
		winUser.Show()
	
	def delUser(self, evt):
		q=YesNo(self.frmSettings, _("Do you want remove this user?"), caption = 'Yes or no?')
		if q==True:
			self.configUsers.remove_section(self.userSelected)
			with open(getConfUsersFilePath(), 'w') as configfile:
				self.configUsers.write(configfile)
			self.loadUsers()
	
	def userSelected(self, evt):
		idx=self.listUsers.GetFirstSelected()
		self.userSelected=self.listUsers.GetItemText(idx,0)
	
	def editUser(self, evt):
		try:
			winUser= formEditUser(self, self.userSelected)
			winUser.Show()
		except Exception as e :
			Warn(self.frmSettings, _("Select a user!"), caption = 'Warning!')
			print(str(e))

	def resetConfiguration(self,evt):
		q=YesNoWarning(self.frmSettings, _("Do you want delete all preferences?"), caption = 'Yes or no?')
		if q==True:
			initConfig()
			os.remove(getConfUsersFilePath())
			self.frmSettings.Close()
			
		
