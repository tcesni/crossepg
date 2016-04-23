#### PROJECT MIGRATION ####

**CrossEPG moved on https://github.com/E2OpenPlugins**





SIFTeam CrossEPG is a lightweight and portable epg for enigma2 dvb receivers (sat, cable and dtt). (c) 2009-2011 Sandro Cavazzoni

#### Generic features: ####
  * A lightweight epg db
  * Protocol supported (by sat): OpenTV, MHW2 (with mhw2downloader by sergiotas)
  * Protocol supported (by file): CSV, XMLTV (also gzip compressed), XEPGDB
  * Scriptable with python
  * HTTP data retrieve (for import)
  * Integration with internal receiver epg
  * Open source (LGPLv2.1 license)
  * Create a compatibile epg.dat
  * Configuration panel
  * Downloader plugin
  * Importer plugin
  * Automatic script execution before import process
  * Automatic daily EPG download
  * Delay daily download if exist a record in progress
  * Automatic EPG download on channel tune
  * Python libraries for developers
  * Automatic load data after a download without a reboot (a patch is required)
  * Automatic reboot enigma2 if no patch exist
  * Support for CrossEPG ENIGMA2 v2 patch
  * Support for simple epgcache.load() patch
  * Support for EDG NEMESIS patch
  * Support for Oudeis patch
  * Support UTF-8 charset
  * Internationalization
#### Default providers: ####
  * Ausat OpenTV (Optusc1 on 156.0)
  * Sky Italia OpenTV (Hotbird on 13.0)
  * Sky Uk OpenTV (Astra2 on 28.2)
  * Sky Uk OpenTV (Astra2 on 28.4)
  * MHW2 Digital+ (mhw2downloader by sergiotas)
  * Ambrosa RAI Script
  * Ambrosa Mediaset Premium Script
  * Devilcosta Nova English XMLTV
  * Devilcosta Nova Greek XMLTV
  * Krkadoni ExYu XMLTV
  * Linuxsat ExUSSR XMLTV
  * Rytec Benelux XMLTV
  * Rytec Bulgaria XMLTV
  * Rytec Denmark XMLTV
  * Rytec Erotic XMLTV
  * Rytec Finland XMLTV
  * Rytec France XMLTV
  * Rytec Germany/Austria/Swiss XMLTV
  * Rytec Greece In English XMLTV
  * Rytec Greece XMLTV
  * Rytec Hungary XMLTV
  * Rytec Israel XMLTV
  * Rytec Italy XMLTV
  * Rytec Norway XMLTV
  * Rytec Osn/Jsc XMLTV
  * Rytec Poland XMLTV
  * Rytec Portugal XMLTV
  * Rytec Romania XMLTV
  * Rytec Serbia/Croatia/Montenegro XMLTV
  * Rytec Slovack/Czech XMLTV
  * Rytec Slovenia XMLTV
  * Rytec Spain XMLTV
  * Rytec Sweden XMLTV
  * Rytec Turkey XMLTV
  * Rytec UK BBCi XMLTV
  * Rytec UK XMLTV
  * Rytec West-Africa/Csat Horizons XMLTV
  * Za/Multichoice/Dstv/Osn XMLTV
#### Application credits: ####
  * Sandro Cavazzoni aka skaman (main developer)
  * Ambrosa (scripts developer)
  * Sergiotas (mhw2epgdownloader author)
  * u Killer Bestia (server side application maintainer)
  * Spaeleus (italian translations)
  * Bodyan (ukrainian translations)
  * Kosmacz (polish translations)
  * Ku4a (russian translations)
#### Sources credits: ####
  * Rytec http://www.rytec.be (xmltv providers for many countries)
  * Krkadoni http://www.krkadoni.com/ (xmltv provider for Ex Yugoslavia)
  * Bodyan and dillinger http://linux-sat.tv/ (xmltv provider for ex USSR channels)
  * Devilcosta http://sgcpm.com/ (xmltv provider for nova channels in greek and english)
#### About CrossEPG ENIGMA2 patch v2 ####
  * The patch add an API crossepgImportEPG(string dbroot) visible on python side.
  * The fix on sectionRead is the same used from oudeis patch and i think is deeply tested.
  * I used oudeis patch as an example to make my patch working... so to oudeis his credits :)

#### Old plugins: ####
  * mp2csv by met67 (download mediaset premium epg from internet)

_If you want support crossepg development please make a donation_
[![](https://www.paypal.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=sandro%40skanetwork%2ecom&lc=IT&item_name=CrossEPG&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)