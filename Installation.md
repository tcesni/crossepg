1. Copy the package in your box.
2. From telnet type:

```
ipkg install crossepg_enigma2-(VERSION)_(ARCHITECTURE).ipk}
```

2. Reboot enigma2 GUI.

### Only for enigma2 previous 20110216 ###

with a unix compatible editor edit the file /usr/bin/enigma2.sh and before the line

```
LD_PRELOAD=/usr/lib/libopen.so.0.0 /usr/bin/enigma2
```

add this line

```
/usr/crossepg/crossepg_epgmove.sh
```