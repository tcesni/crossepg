from enigma import getDesktop, eTimer

from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ProgressBar import ProgressBar

from Screens.Screen import Screen
from Screens.MessageBox import MessageBox

from crossepglib import *
from crossepg_locale import _

import httplib
import xml.etree.cElementTree
import re
import os

RYTEC_HOSTS = ["www.xmltvepg.be", "www.world-of-satellite.com", "www.xmltvepg.nl", "www.tm800hd.co.uk"]
RYTEC_XMLS = ["/rytec.sources.xml", "/epg_data/rytec.sources.xml", "/rytec.sources.xml", "/rytec.sources.xml"]

class CrossEPG_Rytec_Source(object):
	def __init__(self):
		self.channels_urls = []
		self.epg_urls = []
		self.description = ""

class CrossEPG_Rytec_Update(Screen):
	def __init__(self, session):
		if (getDesktop(0).size().width() < 800):
			skin = "%s/skins/downloader_sd.xml" % os.path.dirname(sys.modules[__name__].__file__)
			self.isHD = 0
		else:
			skin = "%s/skins/downloader_hd.xml" % os.path.dirname(sys.modules[__name__].__file__)
			self.isHD = 1
		f = open(skin, "r")
		self.skin = f.read()
		f.close()
		Screen.__init__(self, session)
		
		self.sources = []
		self.session = session
		
		self["background"] = Pixmap()
		self["action"] = Label(_("Updating rytec providers..."))
		self["status"] = Label("")
		self["progress"] = ProgressBar()
		self["progress"].hide()
		
		self.config = CrossEPG_Config()
		self.config.load()
		
		self.timer = eTimer()
		self.timer.callback.append(self.start)
		
		self.onFirstExecBegin.append(self.firstExec)
		
	def firstExec(self):
		if self.isHD:
			self["background"].instance.setPixmapFromFile("%s/images/background_hd.png" % (os.path.dirname(sys.modules[__name__].__file__)))
		else:
			self["background"].instance.setPixmapFromFile("%s/images/background.png" % (os.path.dirname(sys.modules[__name__].__file__)))
		self.timer.start(100, 1)
		
	def start(self):
		if self.load():
			self.save(self.config.home_directory + "/providers/")
			self.session.open(MessageBox, _("%d providers updated") % len(self.sources), type = MessageBox.TYPE_INFO, timeout = 5)	
		else:
			self.session.open(MessageBox, _("Cannot retrieve rytec sources"), type = MessageBox.TYPE_ERROR, timeout = 10)	
		self.close()

	def load(self):
		ret = False
		count = 0
		for host in RYTEC_HOSTS:
			try:
				print "downloading from http://%s%s" % (host, RYTEC_XMLS[count])
				conn = httplib.HTTPConnection(host)
				conn.request("GET", RYTEC_XMLS[count])
				httpres = conn.getresponse()
				if httpres.status == 200:
					f = open ("/tmp/crossepg_rytec_tmp", "w")
					f.write(httpres.read())
					f.close()
					self.loadFromFile("/tmp/crossepg_rytec_tmp")
					os.unlink("/tmp/crossepg_rytec_tmp")
					ret = True
				else:
					print "http error: %d (http://%s%s)" % (httpres.status, host, RYTEC_XMLS[count])
			except Exception, e:
				print e
			count += 1
		return ret

	def getServer(self, description):
		for source in self.sources:
			if source.description == description:
				return source
		return None
			
	def loadFromFile(self, filename):
		mdom = xml.etree.cElementTree.parse(filename)
		root = mdom.getroot()

		for node in root:
			if node.tag == "source":
				source = CrossEPG_Rytec_Source()
				source.channels_urls.append(node.get("channels"))
				for childnode in node:
					if childnode.tag == "description":
						source.description = childnode.text
					elif childnode.tag == "url":
						source.epg_urls.append(childnode.text)

				oldsource = self.getServer(source.description)
				if oldsource == None:
					self.sources.append(source)
				else:
					if len(source.epg_urls) > 0:
						if source.epg_urls[0] not in oldsource.epg_urls:
							oldsource.epg_urls.append(source.epg_urls[0])
					if len(source.channels_urls) > 0:
						if source.channels_urls[0] not in oldsource.channels_urls:
							oldsource.channels_urls.append(source.channels_urls[0])
				
	def save(self, destination):
		os.system("rm -f " + destination + "/rytec_*.conf")
		for source in self.sources:
			p = re.compile('[/:()<>|?*\s-]|(\\\)')
			filename = p.sub('_', source.description).lower()
			if filename[:6] != "rytec_":
				filename = "rytec_" + filename
			f = open(destination + "/" + filename + ".conf", "w")
			f.write("description=" + source.description + "\n")
			f.write("protocol=xmltv\n");
			count = 0
			for url in source.channels_urls:
				f.write("channels_url_" + str(count) + "=" + url + "\n")
				count += 1
				
			count = 0
			for url in source.epg_urls:
				f.write("epg_url_" + str(count) + "=" + url + "\n")
				count += 1
			f.write("preferred_language=eng");
			f.close()
			
