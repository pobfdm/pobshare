#!/usr/bin/env python3
import wx
from wx import xrc
import os
from utils import *
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

class formEditUser():
	
	def __init__(self, gui, user=None):
		
		self.user=user
		self.gui=gui
		self.initConfig()
		
		
		#EditUser Window
		self.res = xrc.XmlResource(os.path.join('gui','main.xrc'))
		self.frmEditUser = self.res.LoadDialog(gui.frmSettings, 'frmEditUser')
		self.txtUsername=xrc.XRCCTRL(self.frmEditUser, 'txtUsername')
		self.txtPassword=xrc.XRCCTRL(self.frmEditUser, 'txtPassword')
		self.dirPickerRootFolder=xrc.XRCCTRL(self.frmEditUser, 'dirPickerRootFolder')
		self.chkReadOnly=xrc.XRCCTRL(self.frmEditUser, 'chkReadOnly')
		self.btSave=xrc.XRCCTRL(self.frmEditUser, 'btSave')
		self.btCancel=xrc.XRCCTRL(self.frmEditUser, 'btCancel')
		
		if (user!=None):
			self.txtUsername.SetValue(self.config[user].name)
			self.txtPassword.SetValue(self.config[user]['password'])
			self.dirPickerRootFolder.SetPath(self.config[user]['root_folder'])
			if (self.config[user]['readonly']=='True'): self.chkReadOnly.SetValue(True)
		
		#Bind widgets
		self.btSave.Bind(wx.EVT_BUTTON, self.Save)
		self.btCancel.Bind(wx.EVT_BUTTON, self.Cancel)
			
			
	def initConfig(self):
		self.config = configparser.ConfigParser()
		self.config.read(getConfUsersFilePath())
	
	def Cancel(self,evt):
		self.frmEditUser.Close()
	
	def Save(self, evt):
		
		if (int(len(self.txtUsername.GetValue()))>3 and int(len(self.txtPassword.GetValue())>3)):
			pass
		else:
			Warn(self.frmEditUser, _("Username and password must be > 3"), caption = 'Warning!')
			self.gui.loadUsers()
			return
			
		if (os.path.isdir(self.dirPickerRootFolder.GetPath())):
			pass
		else:
			Warn(self.frmEditUser, _("The folder must exist!"), caption = 'Warning!')
			self.gui.loadUsers()
			return	
		
		#saving
		self.config.remove_section(self.user)
		usr=self.txtUsername.GetValue()
		self.config.add_section(usr)
		self.config[usr]['password']=self.txtPassword.GetValue()
		self.config[usr]['root_folder']=self.dirPickerRootFolder.GetPath()
		
		if (self.chkReadOnly.GetValue()==True):
			self.config[usr]['readonly']='True'
		else:
			self.config[usr]['readonly']='False'
			
		with open(getConfUsersFilePath(), 'w') as configfile:
			self.config.write(configfile)
		self.gui.loadUsers()
		self.frmEditUser.Close()		
	
	def Show(self):	
		self.frmEditUser.ShowModal()
