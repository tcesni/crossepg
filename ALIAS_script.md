ALIAS script is written using Python language and can work only with Enigma2 STB

It's placed under _crossepg/scripts/alias/_ directory

Suppose you need to copy epg data from a channel to another (i.e. from "RAI UNO" to "RAIUNO") with obviously different SID

CrossEPG has it own "alias" system: you must create a file _crossepg/aliases/somename.conf_ with this content (example):
```
#BBC 1
2|2046|10301,49|76|7609
#BBC 2
2|2045|6302,49|80|8030
#ITV1
2|2044|10100,49|28|17
#CHAN 4
2|2041|9211,49|28|1803
#CHAN 5
2|2037|7700,49|81|8101
#BBC HD
2|2050|6940,49|79|7901
```
values are **onid|tsid|sid** and with this method you can "link" two (or more) channels together. When you add an EPG event for a channel, the same event is copied/linked to the other channel.


But this method is not user-friendly

So I've made a script that do the same: copy epg data from a SOURCE channel to a DESTINATION channel using channel name (as show in your channel list) as reference. Also it can use for SOURCE the **sid-tsid-onid** values

DESTINATION is the channel name as show in your channel list. If there are multiple channel with the same name, epg data are copied to all these channels.

EPG events text (short descr. and long descr.) are really "linked" to channel: it's not a real data "copy". EPG database size will not growth so much

Before use ALIAS script, you need to configure editing _alias.conf_ file

I suggest you to run as last provider. Typical workflow:
  * download data running OpenTV provider
  * download data running script provider (i.e. RAI)
  * do aliases running ALIAS script provider

This is alias.conf documentation
```
# how to setup [aliases] section
#
# format:
# SOURCE=DESTINATION
# epg data will be copied from SOURCE to DESTINATION
#
# SOURCE is:
# channel_name-provider_name
#
#   or
#
# SID-TSID-ONID
# i.e. 0002:00820000:1770:0110:1:0
#       SID:   ns   :TSID:ONID:stype:unused
# SID = 0002  TSID = 1770  ONID = 0110
#
#
# DESTINATION is:
# channel_name[,channel_name...]
#
#
# Examples:
# canale5-mediaset=canale 5
# epg data from "canale 5" provider "mediaset" will be copied to "canale 5" (every provider)
#
# canale5-mediaset=canale 5,canale cinque,canale5
# epg data from "canale 5" provider "mediaset" will be copied to "canale 5" (every provider) and
# to "canale cinque" (every provider) and to "canale5" (same name as source but different provider than "mediaset")
#
# 0002-1770-0110=canale 5
# epg data from sid "0002:00820000:1770:0110:1:0" will be copied to "canale 5" (every provider)
#
# 0002-1770-0110=canale 5,canale cinque,canale5
# epg data from "0002:00820000:1770:0110:1:0"  will be copied to "canale 5" (every provider) and
# to "canale cinque" (every provider) and to "canale5" (every provider)
#
#
#
# note 1: channel_name and provider_name are case insensitive
#
# note 2: SID/TSID/ONID can be read using remote control MENU->INFORMATION->CURRENT CHANNEL INFORMATION
#         ServiceReference looks like 
#         1:0:19:106A:2008:FBFF:820000:0:0: 
#         the format is
#         1:0:19:SID :TSID:ONID:820000:0:0:
#         so the SOURCE will be: 
#         106A-2008-FBFF=.......


# ALIASES configuration section
[aliases]


canale 5-mediaset=canale 5,canale5

```