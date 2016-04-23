RAI script is written using Python language and can work only with Enigma2 STB

It's placed under _crossepg/scripts/rai/_ directory

It set Italy RAI EPG downloading EPG web pages from http://www.rai.it , parse HTML data using sgmllib.py and extracting EPG data. Then EPG data are injected into CrossEPG internal database. Obviously Internet connection is required or rai.it web pages cannot be downloaded.

For each event there is only the "title" (short description) and not "summarie" (long description) because rai.it website has not info about long description. Yes: rai.it is the italian public television broadcast service and users cannot read "summarie". Incredible, isn'it ? And not all RAI channels are present into rai.it website :-((

Warning: some channels are present in different provider. I.e. "RAI STORIA" EPG data are present in OpenTV SkyIT and also in "RAI\_script". You must choose which epg you want because the last provider data overwrite the previous. In my opinion it's better that you run RAI script **after** OpenTV SkyIT


It's configuration is a text file _crossepg/scripts/rai/rai.conf_ and you should have a look before using it. It's well documented.

There are 2 sections inside _rai.conf_

  * the first section is `[`global`]` and usually you dont' change anything.
  * the second section is `[`channels`]` and here you can map rai.it channel ID with your STB channel name. See _rai.conf_ for more infos
