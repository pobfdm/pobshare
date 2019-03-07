#!/usr/bin/env python3
import sys, os, configparser, shutil

def getTempDir():
	import tempfile
	return tempfile.gettempdir()+os.sep

def getLocalIp():
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip= s.getsockname()[0]
	s.close()
	return ip
'''
def getPublicIp():
	import requests
	fip=getTempDir()+"publicip.txt"
	
	url = "http://www.freemedialab.org/myip/index.php"
	r = requests.get(url, allow_redirects=True)
	open(fip, 'wb').write(r.content)
	
	prefs = configparser.ConfigParser()
	prefs.read(fip)
	return prefs['Connessione']['IP']
'''

def pingTCP(host, port):	
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((host, port))
		return True
	except:
		return False
	s.close()


def getHomeDirPath():
	from os.path import expanduser
	home = expanduser("~")
	return home

def getConfigDirPath():
	from os.path import expanduser
	home = expanduser("~")
	if sys.platform == 'win32': 
		configDir=home+"\\AppData\\Local\\pobshare\\"
	elif  sys.platform == 'linux':
		configDir=home+"/.config/pobshare/"
	elif sys.platform== "darwin":
		configDir=home+"/.config/pobshare/"	
	else:
		configDir=home+"/.config/pobshare/"
	
	return configDir 

def getDatetime():
	from time import gmtime, strftime
	return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def getConfGeneralFilePath():
	p=getConfigDirPath()+"general.conf"
	return p

def getConfUsersFilePath():
	p=getConfigDirPath()+"users.conf"
	return p

def initConfig():
	confDir=getConfigDirPath()
	confGeneralFile=getConfGeneralFilePath()
	
	if (not os.path.isdir(confDir)):
		os.makedirs(confDir)
	if (not os.path.isfile(confGeneralFile)):
		config = configparser.ConfigParser()
		config.add_section('general')
		config['general']['enable_at_startup'] = 'False'
		config['general']['run_server_at_start'] = 'False'
		config['general']['ftp_port'] = '2121'
		config.add_section('anonymous')
		config['anonymous']['enable'] = 'True'
		config['anonymous']['readonly'] = 'False'
		config['anonymous']['root_folder'] =  getHomeDirPath()
		
		
		
		with open(confGeneralFile, 'w') as configfile:
			config.write(configfile)

def getAutorunFolder():
	if sys.platform=="win32":
		return getHomeDirPath()+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
	if  sys.platform == 'linux':
		return getHomeDirPath()+"/.config/autostart/"


def createWinShortcut(src, link, workingDir, icon):    
	vbscript='''
	Set oWS = WScript.CreateObject("WScript.Shell")
	sLinkFile = "%s"
	Set oLink = oWS.CreateShortcut(sLinkFile)
		oLink.TargetPath = "%s"
	 '  oLink.Arguments = ""
	   oLink.Description = "Pobkupd.  The Pobkup deamon "   
	 '  oLink.HotKey = "ALT+CTRL+F"
	   oLink.IconLocation = "%s, 2"
	 '  oLink.WindowStyle = "1"   
	   oLink.WorkingDirectory = "%s"
	oLink.Save
	''' % (link, src, icon, workingDir)
	path=getTempDir()+'createShortcut.vbs'
	print(vbscript,  file=open(path, 'w'))
	os.system(path)
	
def EnableAutorunAtLogin():
	if  sys.platform == 'linux':
		src="/usr/share/applications/pobshare.desktop"
		dst=getAutorunFolder()+"pobshare.desktop"
		try:
			shutil.copyfile(src, dst)
		except Exception as e :
			print(str(e))				
	
	
	if  sys.platform == 'win32':
		if getattr(sys, 'frozen', False):
			# frozen
			src=os.path.join(os.path.dirname(sys.executable),"pobshare.exe") 
			dst=getAutorunFolder()+"pobshare.lnk"
			rootDir=os.path.join(os.path.dirname(sys.executable))
			icon=os.path.join(os.path.dirname(sys.executable),"pobshare.exe") 
		else:
			# unfrozen
			src=os.path.join(os.path.dirname(os.path.realpath(__file__)),"pobshare.py")
			dst=getAutorunFolder()+"pobshare.lnk"
			rootDir=os.path.join(os.path.dirname(os.path.realpath(__file__)))
			icon=sys.executable
		
		createWinShortcut(src,dst,rootDir,icon)
		
	if (os.path.isfile(dst)):
		return True
	else:
		return False


def DisableAutorunAtLogin():
	if  sys.platform == 'linux':
		dst=getAutorunFolder()+"pobshare.desktop"
		if (os.path.isfile(dst)):
			os.remove(dst)	
		if (not os.path.isfile(dst)):
			return True
		else:	
			return False		

	if  sys.platform == 'win32':
		if getattr(sys, 'frozen', False):
			# frozen
			dst=getAutorunFolder()+"pobshare.lnk"
		else:
			# unfrozen
			dst=getAutorunFolder()+"pobshare.lnk"
		
		if (os.path.isfile(dst)):
			os.remove(dst)	
		if (not os.path.isfile(dst)):
			return True
		else:	
			return False

#print(getAutorunFolder())
