#!/usr/bin/python
# rai.py  by Ambrosa http://www.ambrosa.net
# this module is used for download EPG data from Rai website
# derived from E2_LOADEPG

__author__ = "ambrosa http://www.ambrosa.net"
__version__ = "0.01 beta CrossEPG"
__copyright__ = "Copyright (C) 2008-2010 Alessandro Ambrosini"
__license__ = "CreativeCommons by-nc-sa http://creativecommons.org/licenses/by-nc-sa/3.0/"

import os
import sys
import time
import codecs
import socket
import string
import random
import urllib2
import ConfigParser

# import CrossEPG functions
import crossepg

# location of local python modules under "scripts/" dir.
# add it to sys.path()
crossepg_instroot = crossepg.epgdb_get_installroot()
if crossepg_instroot == False:
	sys.exit(1)
scriptlib = os.path.join(crossepg_instroot , 'scripts/lib')
sys.path.append(scriptlib)

# import local modules
import sgmllib
import stuff

# =================================================================
# HTML PARSER

class Titolo_parser(sgmllib.SGMLParser):

	def parse(self, s):
		self.feed(s)
		self.close()

	def __init__(self, day_get, verbose=0):
		sgmllib.SGMLParser.__init__(self, verbose)
		self.daynow=day_get
		self.daynext=time.strftime("%Y%m%d",time.localtime(time.mktime(time.strptime(day_get,"%Y%m%d"))+86400))
		self.day=self.daynow
		self.guidatoday = []
		self.guidatomorrow = []
		self.sera = False
		self.tomorrow = False
		self.start_orario = False
		self.start_titolo = False
		self.inside_a_titolo = False
		self.inside_palinsesto = False


	def start_div(self,attributes):
		for name,value in attributes:
			if name == "class":
				if value == "intG":
					self.inside_palinsesto = True

	def start_span(self, attributes):
		if self.inside_palinsesto == True:
			for name, value in attributes:
				if name == "class":
					if value == "ora":
						self.start_orario = True
					if value == "info":
						self.start_titolo = True

	def start_a(self,attributes):
		if self.inside_palinsesto == True:
			if self.start_titolo == True:
				self.inside_a_titolo = True

	def handle_data(self, data):
		if self.inside_palinsesto == True:

			if self.start_orario == True:

				if int(time.strftime("%H",time.strptime(data,"%H:%M"))) > 19 and self.sera == False:
					self.sera = True

				if int(time.strftime("%H",time.strptime(data,"%H:%M"))) < 8 and self.sera == True:
					self.day = self.daynext
					self.tomorrow = True

				self.dataoraevento = time.strftime("%Y-%m-%d %H:%M",time.strptime(self.day+'-'+data,"%Y%m%d-%H:%M"))
				self.start_orario = False

			if self.inside_a_titolo == True:
				if self.tomorrow == False:
					self.guidatoday.append((self.dataoraevento,data.strip()))
				else:
					self.guidatomorrow.append((self.dataoraevento,data.strip()))

				self.inside_a_titolo = False
				self.start_titolo = False
				self.inside_palinsesto = False


	def get_guida(self):
		return ((self.guidatoday,self.guidatomorrow))


# =================================================================



class main:

	# main config file
	CONF_CONFIGFILENAME = "rai.conf"

	# log file
	CONF_LOGFILENAME = "rai.log.txt"

	# Network socket timeout (in seconds)
	CONF_SOCKET_TIMEOUT = 20

	# retry number if HTTP error
	HTTP_ERROR_RETRY = 4
	# seconds to wait between retries
	HTTP_ERROR_WAIT_RETRY = 3

	# random time delay (in seconds) between access to remote web pages
	CONF_RANDOM_MIN = 1.0
	CONF_RANDOM_MAX = 2.0

	# unicode used in epg data
	EPG_CHARSET = 'iso-8859-15'

	TODAY = ''
	DAYCACHE = []
	FIELD_SEPARATOR = '###'
	CHANNELLIST = {}

	def log(self,s):
		crossepg.log_add(s)
		self.logging.log2file(s)


	def __init__(self,confdir,dbroot):

		self.CROSSEPG_DBROOT = dbroot

		LOG_FILE = os.path.join(confdir, self.CONF_LOGFILENAME)
		self.logging = stuff.logging_class(LOG_FILE)

		CONF_FILE = os.path.join(confdir,self.CONF_CONFIGFILENAME)
		if not os.path.exists(CONF_FILE) :
			self.log("ERROR: %s not present" % CONF_FILE)
			sys.exit(1)

		config = ConfigParser.ConfigParser()
		config.optionxform = str  # needed to return case sensitive index
		config.read(CONF_FILE)

		# reading [global] section options
		self.CONF_DEFAULT_PROVIDER = config.get("global","DEFAULT_PROVIDER")
		self.CONF_CACHEDIR = os.path.join(dbroot,config.get("global","CACHE_DIRNAME"))
		self.CONF_MAX_DAY_EPG = config.getint("global","MAX_DAY_EPG")
		self.CONF_URL = config.get("global","URL")

		self.CONF_GMT_ZONE = config.get("global","GMT_ZONE")
		if self.CONF_GMT_ZONE.strip(' ').lower() == 'equal':
			self.DELTA_UTC = -stuff.delta_utc() # return negative if timezone is east of GMT (like Italy)
		else:
			self.DELTA_UTC = float(self.CONF_GMT_ZONE)*3600.0
			if self.DELTA_UTC >= 0:
				self.DELTA_UTC = self.DELTA_UTC + stuff.delta_dst()
			else:
				self.DELTA_UTC = self.DELTA_UTC - stuff.delta_dst()

		self.DELTA_UTC = int(self.DELTA_UTC)
		self.log("Delta UTC = %d seconds" % self.DELTA_UTC)

		if not os.path.exists(self.CONF_CACHEDIR):
			self.log("Creating \'%s\' directory for caching" % self.CONF_CACHEDIR)
			os.mkdir(self.CONF_CACHEDIR)

		# reading [channels] section
		temp=config.items("channels");

		# create a dictionary (Python array) with index = channel ID
		for i in temp:
			self.CHANNELLIST[i[0]]=unicode(i[1],'utf-8')

		if len(self.CHANNELLIST) == 0 :
			self.log("ERROR: [channels] section empty ?")
			sys.exit(1)

		# set network socket timeout
		socket.setdefaulttimeout(self.CONF_SOCKET_TIMEOUT)

		# initialize random generator
		random.seed()

		# create a list filled with dates (format AAAAMMDD) from today to today+ MAX_DAY_EPG
		self.TODAY=time.strftime("%Y%m%d")

		# create a list filled with dates (format _AAAA_MM_DD) from today to today+ MAX_DAY_EPG
		self.TODAYRS=time.strftime("_%Y_%m_%d")

		self.DAYCACHE=[self.TODAY]
		for day in range(1,self.CONF_MAX_DAY_EPG):
			self.DAYCACHE.append(time.strftime("%Y%m%d",time.localtime(time.time()+86400*day)))

# ---------


	def download_and_cache(self):

		self.log("Removing old cached files")
		stuff.cleanup_oldcachedfiles(self.CONF_CACHEDIR, self.FIELD_SEPARATOR)

		self.log("Start downloading HTML data from \'%s\'" % self.CONF_URL)

		chlist = self.CHANNELLIST

		# get remote XML files
		#   chid format: channel id , 0|1|2(,new name)
		#   i.e. ("101" , "1,SkyCinema1")
		for c in sorted(chlist.keys()):
			self.guidatoday = []
			self.guidatomorrow = []

			# get cacheopt
			#  0 : don't download/cache
			#  1 : download and cache (optional 1,new_name )
			#  2 : always download overwriting existing files (optional 2,new_name )
			#  3 : always download overwriting existing files only for TODAY (optional 3,new_name )

			cacheopt = int(string.split(chlist[c],",")[0])

			# if cacheopt == 0, do nothing
			if cacheopt == 0:
				continue

			channel_name = ''
			if len(chlist[c].split(",")) > 1 :
				if chlist[c].split(",")[1] != '' :
					# channel renamed, new name provided by user
					channel_name = chlist[c].split(",")[1].strip(' ').lower()

			# if channel name is not present as option, quit with error
			if channel_name == '':
				self.log("ERROR ! ID=%s channel name not present" % c)
				sys.exit(1)

			channel_provider = self.CONF_DEFAULT_PROVIDER
			if len(chlist[c].split(",")) > 2 :
				if chlist[c].split(",")[2] != '' :
					channel_provider = chlist[c].split(",")[2].strip(' ').lower()

			for day in self.DAYCACHE:
				day_get = time.strftime("%Y_%m_%d",time.strptime(day,"%Y%m%d"))
				xmlfile = "?%s_%s" % (c,day_get)

				# download only if file doesn't exist or cacheopt == 2 (always download),
				# using open(...,"w") files will be overwritten (saving a delete + create)

				eventfilename = stuff.fn_escape(str(c) + self.FIELD_SEPARATOR + channel_name + self.FIELD_SEPARATOR + day)
				eventfilepath = os.path.join(self.CONF_CACHEDIR, eventfilename)
				if (cacheopt == 1) and  os.path.exists(eventfilepath):
					continue
				if (cacheopt == 3) and os.path.exists(eventfilepath) and (day != self.TODAY):
					continue

				self.log("Download HTML data from \'%s\'" % (self.CONF_URL + xmlfile))

				i = self.HTTP_ERROR_RETRY
				while i > 0  :
					# to avoid overloading URL website, wait randomly
					time.sleep(random.uniform(self.CONF_RANDOM_MIN, self.CONF_RANDOM_MAX))

					try:
						sock=urllib2.urlopen(self.CONF_URL + xmlfile)
						data=sock.read()

					except IOError, e:
						serr="unknown"
						if hasattr(e, 'reason'):
							serr=str(e.reason)
						elif hasattr(e, 'code'):
							serr=str(e.code)
							if hasattr(e, 'msg'):
								serr+=" , "+str(e.msg)

						self.log("\'%s\' connection error. Reason: %s. Waiting %d sec. and retry [%d] ..." % (self.CONF_URL + xmlfile, serr, self.HTTP_ERROR_WAIT_RETRY, i))
						time.sleep(self.HTTP_ERROR_WAIT_RETRY) # add sleep
						i -= 1

					else:
						i = 0 # force quit WHILE loop
						sock.close()

						dtparser = Titolo_parser(day)
						dtparser.parse(data)
						self.guida = self.guidatomorrow
						(self.guidatoday, self.guidatomorrow) = dtparser.get_guida()
						self.guida = self.guida + self.guidatoday


						self.log("  writing in cache \'%s\'" % eventfilename)
						fd = codecs.open(eventfilepath, "w", 'utf-8')
						fd.write(str(c) + self.FIELD_SEPARATOR + channel_name + self.FIELD_SEPARATOR + channel_provider + self.FIELD_SEPARATOR + day + '\n')
						fd.write("Local Time (human readeable)###Unix GMT Time###Event Title###Event Description\n")

						# extract all events and put in eventfile
						for event in self.guida:
							(dataora,titolo) = event
							event_starttime = dataora
							event_startime_unix_gmt=str(int(time.mktime(time.strptime(event_starttime,"%Y-%m-%d %H:%M"))) - self.DELTA_UTC )

							event_title = unicode(titolo,"utf-8")
							event_title = event_title.replace('\r','')
							event_title = event_title.replace('\n',' ')
							event_title = event_title.strip(' ')
							#event_title=event_title.encode('ascii','replace')

							event_description = ''

							#event_description=event_description.encode('ascii','replace')

							fd.write(event_starttime + self.FIELD_SEPARATOR + event_startime_unix_gmt + self.FIELD_SEPARATOR + event_title + self.FIELD_SEPARATOR + event_description + '\n')


						fd.close()


	def process_cache(self):
		if not os.path.exists(self.CONF_CACHEDIR):
			self.log("ERROR: %s not present" % self.CONF_CACHEDIR)
			sys.exit(1)

		self.log("Loading lamedb")
		lamedb = stuff.lamedb_class()

		self.log("Initialize CrossEPG database")
		crossdb = stuff.crossepg_db_class()
		crossdb.open_db(self.CROSSEPG_DBROOT)

		events = []
		previous_f = ''
		channels_name = ''

		self.log("Start data processing")
		filelist = sorted(os.listdir(self.CONF_CACHEDIR))
		filelist.append('***END***')

		for f in filelist :
			if previous_f == '':
				previous_f = f

			if f != previous_f :
				self.log("processed \'%s\'" % f)

				for c in channels_name:
					sidbyname = lamedb.get_sid_byname(c.strip(' \n').lower())
					if len(sidbyname) == 0:
						continue

					for s in sidbyname:
						# return the list [sid,tsid,onid]
						ch_sid = lamedb.convert_sid(s)

						# add channel into db and get a reference to the structure
						# doesn't matter if the channel already exist... epgdb do all the work
						crossdb.add_channel(ch_sid)

						i = 0
						L = len(events) - 1
						for e in events:

							e_starttime = int(e.split(self.FIELD_SEPARATOR)[1])

							if i < L :
								e_length = int(events[i+1].split(self.FIELD_SEPARATOR)[1]) - e_starttime
							else:
								# last event, dummy length 90 min.
								e_length = 5400
							i += 1

							e_title = e.split(self.FIELD_SEPARATOR)[2]

							# RAI website HAVE NOT long description. (bleah !)
							e_summarie = ' '

							# add_event(start_time , duration , title , summarie , ISO639_language_code , using_UTF8 )
							crossdb.add_event(e_starttime, e_length, e_title, e_summarie, 'ita', False)

				if f == '***END***':
					break

				events = []
				previous_f = f
				channels_name = ''


			if f == previous_f:
				# read events and insert them in events list
				fd = codecs.open(os.path.join(self.CONF_CACHEDIR, f),"r","utf-8")
				temp = fd.readlines()
				fd.close()
				if channels_name == '':
					channels_name = temp[0].split(self.FIELD_SEPARATOR)[1].split('|')
				events.extend(temp[2:])


		crossdb.close_db()

# ****************************************************************************************************************************


# MAIN CODE: SCRIPT START HERE


# get CrossEPG installation dir.
crossepg_instroot = crossepg.epgdb_get_installroot()
if crossepg_instroot == False:
	sys.exit(1)
scriptlocation = os.path.join(crossepg_instroot , 'scripts/rai/')

# get where CrossEPG save data and use it as script cache repository
crossepg_dbroot = crossepg.epgdb_get_dbroot()
if crossepg_dbroot == False:
	sys.exit(1)

# run script class
script_class = main(scriptlocation , crossepg_dbroot)
script_class.download_and_cache()
script_class.process_cache()

