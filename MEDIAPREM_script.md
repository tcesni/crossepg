MEDIAPREM script is written using Python language and can work only with Enigma2 STB

It's placed under _crossepg/scripts/mediaprem/_ directory

It set Italy Mediset Premium EPG downloading EPG data (a single XML file 2 MB size) from MP website, parse XML data using sgmllib.py and extracting EPG data.

XML file has titles but not summaries, so for every event is opened a web page and then summarie is extracted from HTML using sgmllib

Then EPG data are injected into CrossEPG internal database. Obviously Internet connection is required or Mediaset Premium XML file and web pages cannot be downloaded.

It's configuration is a text file _crossepg/scripts/mediaprem/mediaprem.conf_ and you should have a look before using it. It's well documented.

There are 2 sections inside _mediaprem.conf_

  * the first section is `[`global`]` and usually you dont' change anything
  * the second section is `[`channels`]` and here you can map  channel ID with your STB channel name. See _mediaprem.conf_ for more infos

There are many ways to process an XML file. A good way is to use XML.MINIDOM Python module but it's very memory hungry: 40MB RAM for a single 2 MB XML file. It's ok in a personal computer environment but not in a STB device.

Another very simple way is to use SGMLLIB: not very confortable, slowest than MINIDOM but it works fine without any strange memory allocation.

MEDIAPREM script use SGMLLIB but I've made a version using XML.MINIDOM : you can find it for your convenience _crossepg/scripts/mediaprem/example-mediaprem-minidom.conf_ Don't use it: is only as example for other people that want to parse XML data using MINIDOM