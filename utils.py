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

def initCert():
	cert= '''-----BEGIN RSA PRIVATE KEY-----
MIICXwIBAAKBgQC8ddrhm+LutBvjYcQlnH21PPIseJ1JVG2HMmN2CmZk2YukO+9L
opdJhTvbGfEj0DQs1IE8M+kTUyOmuKfVrFMKwtVeCJphrAnhoz7TYOuLBSqt7lVH
fhi/VwovESJlaBOp+WMnfhcduPEYHYx/6cnVapIkZnLt30zu2um+DzA9jQIDAQAB
AoGBAK0FZpaKj6WnJZN0RqhhK+ggtBWwBnc0U/ozgKz2j1s3fsShYeiGtW6CK5nU
D1dZ5wzhbGThI7LiOXDvRucc9n7vUgi0alqPQ/PFodPxAN/eEYkmXQ7W2k7zwsDA
IUK0KUhktQbLu8qF/m8qM86ba9y9/9YkXuQbZ3COl5ahTZrhAkEA301P08RKv3KM
oXnGU2UHTuJ1MAD2hOrPxjD4/wxA/39EWG9bZczbJyggB4RHu0I3NOSFjAm3HQm0
ANOu5QK9owJBANgOeLfNNcF4pp+UikRFqxk5hULqRAWzVxVrWe85FlPm0VVmHbb/
loif7mqjU8o1jTd/LM7RD9f2usZyE2psaw8CQQCNLhkpX3KO5kKJmS9N7JMZSc4j
oog58yeYO8BBqKKzpug0LXuQultYv2K4veaIO04iL9VLe5z9S/Q1jaCHBBuXAkEA
z8gjGoi1AOp6PBBLZNsncCvcV/0aC+1se4HxTNo2+duKSDnbq+ljqOM+E7odU+Nq
ewvIWOG//e8fssd0mq3HywJBAJ8l/c8GVmrpFTx8r/nZ2Pyyjt3dH1widooDXYSV
q6Gbf41Llo5sYAtmxdndTLASuHKecacTgZVhy0FryZpLKrU=
-----END RSA PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIICpzCCAhCgAwIBAgIJAP+qStv1cIGNMA0GCSqGSIb3DQEBBQUAMIGJMQswCQYD
VQQGEwJVUzERMA8GA1UECBMIRGVsYXdhcmUxEzARBgNVBAcTCldpbG1pbmd0b24x
IzAhBgNVBAoTGlB5dGhvbiBTb2Z0d2FyZSBGb3VuZGF0aW9uMQwwCgYDVQQLEwNT
U0wxHzAdBgNVBAMTFnNvbWVtYWNoaW5lLnB5dGhvbi5vcmcwHhcNMDcwODI3MTY1
NDUwWhcNMTMwMjE2MTY1NDUwWjCBiTELMAkGA1UEBhMCVVMxETAPBgNVBAgTCERl
bGF3YXJlMRMwEQYDVQQHEwpXaWxtaW5ndG9uMSMwIQYDVQQKExpQeXRob24gU29m
dHdhcmUgRm91bmRhdGlvbjEMMAoGA1UECxMDU1NMMR8wHQYDVQQDExZzb21lbWFj
aGluZS5weXRob24ub3JnMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC8ddrh
m+LutBvjYcQlnH21PPIseJ1JVG2HMmN2CmZk2YukO+9LopdJhTvbGfEj0DQs1IE8
M+kTUyOmuKfVrFMKwtVeCJphrAnhoz7TYOuLBSqt7lVHfhi/VwovESJlaBOp+WMn
fhcduPEYHYx/6cnVapIkZnLt30zu2um+DzA9jQIDAQABoxUwEzARBglghkgBhvhC
AQEEBAMCBkAwDQYJKoZIhvcNAQEFBQADgYEAF4Q5BVqmCOLv1n8je/Jw9K669VXb
08hyGzQhkemEBYQd6fzQ9A/1ZzHkJKb1P6yreOLSEh4KcxYPyrLRC1ll8nr5OlCx
CMhKkTnR6qBsdNV0XtdU2+N25hqW+Ma4ZeqsN/iiJVCGNOZGnvQuvCAGWF8+J/f/
iHkC6gGdBJhogs4=
-----END CERTIFICATE-----'''
	f=open(getConfigDirPath()+"keycert.pem",'w')
	f.write(cert)
	f.close()


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
		config['general']['enable_ftps'] = 'False'
		initCert()
		config['general']['ssl_cert'] = getConfigDirPath()+"keycert.pem"
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

def checkCert(certFile):
	import OpenSSL.crypto 
	try:
		cert = OpenSSL.crypto.load_certificate(
			OpenSSL.crypto.FILETYPE_PEM, 
			open(certFile).read()
		)
		return True
	
	except Exception as e:
		return str(e)
			

