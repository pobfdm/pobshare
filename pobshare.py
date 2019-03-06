#!/usr/bin/env python3
import wx
import wx.adv
from wx import xrc
import sys, os
from guiUtils import *
from utils import *
from ftpServer import *
import threading

TRAY_TOOLTIP = 'Pobshare help you to share a folder' 
TRAY_ICON = os.path.join('icons','small','pobshare-gray.png')


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
	def __init__(self, gui):
		self.gui = gui
		super(TaskBarIcon, self).__init__()
		self.set_icon(TRAY_ICON)
		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

	def CreatePopupMenu(self):
		menu = wx.Menu()
		create_menu_item(menu, 'Start/Stop Server', self.startStopServer)
		menu.AppendSeparator()
		create_menu_item(menu, 'Exit', self.on_exit)
		return menu

	def set_icon(self, path):
		icon = wx.Icon(path)
		self.SetIcon(icon, TRAY_TOOLTIP)

	def on_left_down(self, event):      
		#print ('Tray icon was left-clicked.')
		if (self.gui.mainFrame.IsShown()):
			self.gui.mainFrame.Show(False)
		else:
			self.gui.mainFrame.Show(True) 

	def startStopServer(self, evt):
		self.gui.threadFTPserver = threading.Thread(target=self.gui.startStopServer, args=())
		self.gui.threadFTPserver.daemon = True
		self.gui.threadFTPserver.start()
		 
	def on_exit(self, event):
		wx.CallAfter(self.Destroy)
		self.gui.mainFrame.Close()

 
class PobShare(wx.App):
 
	def OnInit(self):
		self.res = xrc.XmlResource(os.path.join('gui','main.xrc'))
		self.init_frame()
		return True
	
	def init_frame(self):
		# Main window
		self.mainFrame = self.res.LoadFrame(None, 'mainFrame')
		self.mainFrame.SetIcon(wx.Icon(os.path.join("icons","pobshare.ico")))
		self.trayIcon=TaskBarIcon(self)
		
		#Getting widgets
		self.btStartStop=xrc.XRCCTRL(self.mainFrame, 'btStartStop')
		self.statusBar=xrc.XRCCTRL(self.mainFrame, 'statusBar')
		self.listCtrlStatus=xrc.XRCCTRL(self.mainFrame, 'listCtrlStatus')
		self.listCtrlStatus.AppendColumn( 'Log',  width=350)
		self.txtUrl=xrc.XRCCTRL(self.mainFrame, 'txtUrl')
		self.btShareUrl=xrc.XRCCTRL(self.mainFrame, 'btShareUrl')
		
		#Getting menu
		self.menubar = self.mainFrame.GetMenuBar()
		self.mnuItemExit = self.menubar.FindItemById(xrc.XRCID('mnuItemExit'))
		self.mnuItemSettings = self.menubar.FindItemById(xrc.XRCID('mnuItemSettings'))    
		
		#Bind event Menu
		self.mainFrame.Bind(wx.EVT_MENU, self.quit, self.mnuItemExit)
		self.mainFrame.Bind(wx.EVT_MENU, self.showSettings, self.mnuItemSettings)
		
		#Bind Main Window event
		self.mainFrame.Bind(wx.EVT_CLOSE, self.quit)
		
		#Bind widgets
		self.btStartStop.Bind(wx.EVT_BUTTON, self.onStartStopClicked)
		self.btShareUrl.Bind(wx.EVT_BUTTON, self.copyUrl)
		
		#Access to general config
		self.generalConfig()
		
		if (self.prefs['general']['run_server_at_start']=='False'):
			self.mainFrame.Show(True)
		else:
			self.mainFrame.Show(False)
			self.threadFTPserver = threading.Thread(target=self.startStopServer, args=())
			self.threadFTPserver.daemon = True
			self.threadFTPserver.start()	
	
	def copyUrl(self, evt):
		text = self.txtUrl.FindFocus()
		if text is not None:
			self.txtUrl.SelectAll()
			self.txtUrl.Copy()
	
	def generalConfig(self):
		self.prefs = configparser.ConfigParser()
		self.prefs.read(getConfGeneralFilePath())
	
	def onStartStopClicked(self, evt):
		self.threadFTPserver = threading.Thread(target=self.startStopServer, args=())
		self.threadFTPserver.daemon = True
		self.threadFTPserver.start()
				
		
	def startStopServer(self):
		if not hasattr(self, 'ftpServer'):
			self.ftpServer=TFtpServer(self)
		if (self.ftpServer.started==False):
			self.ftpServer.start()
		else:
			self.ftpServer.stop()
	
	def serverFailed(self, msg):
		redSmall = wx.Bitmap(os.path.join('icons','small','pobshare-red.png'), wx.BITMAP_TYPE_ANY)
		self.trayIcon.set_icon(redSmall)
		self.btStartStop.SetBitmap(redSmall)
		self.statusBar.SetStatusText(str(msg))
		self.mnuItemSettings.Enable(True)
	
	def serverStarted(self):
		self.generalConfig()
		greenSmall = wx.Bitmap(os.path.join('icons','small','pobshare-green.png'), wx.BITMAP_TYPE_ANY)
		self.trayIcon.set_icon(greenSmall)
		self.btStartStop.SetBitmap(greenSmall)
		self.txtUrl.SetValue('ftp://%s:%s' % (getLocalIp(), self.prefs['general']['ftp_port']))
		self.statusBar.SetStatusText(_("Server started.")) 
		self.mnuItemSettings.Enable(False)
	
	def serverNormal(self):
		graySmall = wx.Bitmap(os.path.join('icons','small','pobshare-gray.png'), wx.BITMAP_TYPE_ANY)
		self.trayIcon.set_icon(graySmall)
		self.btStartStop.SetBitmap(graySmall)
		self.statusBar.SetStatusText(_("Server stopped.")) 
		self.mnuItemSettings.Enable(True) 	
		
	def quit(self, evt):
		r= YesNo(self.mainFrame, _("Do you want exit?"), caption = 'Exit')
		if (r==True):
			self.Destroy()
			sys.exit()
		
	def showSettings(self, evt):
		import settingsGui
		pobshareSettings= settingsGui.formSettings(self.mainFrame)
		pobshareSettings.Show()
   
 
 
if __name__ == '__main__':
	#Gettex
	import locale, gettext
	try:
		current_locale, encoding = locale.getdefaultlocale()
		locale_path = 'locale'
		language = gettext.translation ('pobshare', locale_path, [current_locale] )
		language.install()
		
	except:
		_ = gettext.gettext
	
	#Init
	initConfig()
	
	
	app =  PobShare(False)
	app.MainLoop()
