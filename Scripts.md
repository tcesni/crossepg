# INTRODUCTION #
CrossEPG can run scripts during provider download process. Scripts can download complex data (i.e. download epg data from a website, parse HTML code and then inject data into CrossEPG internal database), do some task (i.e. do epg data aliasing, simple print "Hello World") and much more.

Scripts can be anything: shell code, binary, Python code .....

Only using Python code you can access to CrossEPG API and access to its functions. Obviously Python code works ONLY with Enigma2 Set-Top-Box (i.e. Dreambox 7025, 800, 8000 ..., DuoLabs QboxHD, QBoxMINI, ...)

The goal is to merge Ambrosa E2\_LOADEPG http://www.ambrosa.net with CrossEPG

This document is focused to describe how to develop Python scripts but some item are the same for other script type (see BASICS below)

## BASICS ##
Creating a script require some steps

1)
Make your Python script. The script must be placed under _crossepg/scripts/_ directory.
It's better if you create a subdir under _crossepg/scripts/_ and put there your files

Your script can import some CrossEPG functions (see below) and/or can import some _scriptlib_ function (see below)

2)
Add your script as a new "script provider". You must create a 3 lines text file _your\_script.conf_ and place into _crossepg/providers/_

The first line is **protocol=script**

The second line is **filename=** follow by script path relative to _crossepg/scripts/_

The third line is **description=** follow by a text message that will be show in OSD
```
protocol=script
filename=YOURSCRIPT_RELATIVE_PATH.PY
description=A TEXT WITH SCRIPT DESCRIPTION
```

Example _crossepg/providers/test\_script.conf_
```
protocol=script
filename=test.py
description=example test script (do nothing)
```

Example _crossepg/providers/rai\_script.conf_
```
protocol=script
filename=rai/rai.py
description=Italy RAI website (see scripts/rai/rai.conf)
```

## CROSSEPG LIBRARY ##
CrossEPG exports some internal functions. These functions can be imported and used in your Python script
```
import crossepg
```

You can find the exported functions full list into _/usr/lib/python/crossepg.py_ . This path can change because STB devices use different filesystem layout

In QboxHD and QboxMINI device the path is _/usr/local/lib/python2.6/crossepg.py_

The main useful functions are:
  * crossepg.epgdb\_get\_installroot() : the path to main CrossEPG installation dir
  * crossepg.epgdb\_get\_dbroot() : the path to CrossEPG database
  * crossepg.epgdb\_open(dbroot) : open CrossEPG database located under _dbroot_ path
  * crossepg.epgdb\_close() : close CrossEPG database
  * crossepg.log\_open(dbroot) : open _crossepg.log_ file located under _dbroot_
  * crossepg.log\_add("text") : print a log messages to STDOUT and, if previously opened, add to main _crossepg.log_ file
  * and much more ....

You can find examples inside _crossepg/scripts/example\_script.py_ and _crossepg/scripts/test.py_ . View other examples into SCRIPTLIB (see below), RAI script, ALIAS script.

## SCRIPTLIB LIBRARY ##
For your convenience I've made a Python lib _crossepg/scripts/lib/scriptlib.py_ that simplify the access to some CrossEPG native function and add other useful functions

Because _scriptlib.py_ path is not known by Python, it's required to add the full _scripts/lib_ path to the environment var PATH before "import" it
```
import os
import sys
import crossepg
# location of local Python modules under "scripts/lib" and add it to sys.path()
crossepg_instroot = crossepg.epgdb_get_installroot()
if crossepg_instroot == False:
	sys.exit(1)
libdir = os.path.join(crossepg_instroot , 'scripts/lib')
sys.path.append(libdir)

# import scriptlib module
import scriptlib
```

Under _scripts/lib/_ I've added other generic Python module, i.e. _markupbase.py_ and _sgmllib.py_ (very useful for parsing HTML data) because some STB have not in their standard Python tree.

Because _scripts/lib_ is added into PATH as last item, if the module exists in your standard Python tree, it will be used. If not, it will be loaded from _scripts/libs/_

_scripts/lib/_ is the right place to put extra libs or some Python standard module not present in every STB (like _sgmllib.py_)

These are some functions and classes. View inside _scriptlib.py_ for details:

  * def fn\_escape() : remove strange chars from filename converting into `_` (underscore)
  * class logging\_class : logging facility
  * class zlib\_class : uncompress gzipped file using gzip command
  * def delta\_utc() : return localtime - utctime difference
  * def delta\_dst() : return DST time difference
  * class lamedb\_class : parse lamedb and load into an array
  * class crossepg\_db\_class : aggregate some CrossEPG functions and make easy to access to CrossEPG internal database

## EXECUTING AND DEBUGGING YOUR SCRIPT ##
crossepg library and scriptlib library can work outside Enigma2 so you can run your script by hand for debugging purpose
```
# go into your script directory
cd /var/crossepg/scripts/rai/
# and run it
./rai.py
```
and see what happen

Or use the more complex way with _crossepg\_downloader_ binary testing it as a real provider (checking _your\_script.conf_ )
```
cd /var/crossepg
# run script provider. it's the crossepg/provider/script_name.conf without '.conf'
./crossepg_downloader -p rai_script
```
When your script is working fine, you can add it as a download provider using CrossEPG Config Menu plugin.

Your script is a download provider and it will be executed as a provider but it can download nothing and do nothing. It can do some tasks (i.e. simple print "Hello world !") without accessing to CrossEPG database or accessing to anything else.

Providers execution order can be easy selected using CrossEPG Config Menu plugin (since svn 196) so user can choose if it's better that your script should be run BEFORE or AFTER other provider.

## LOGGING FACILITY ##
Log is made easy using _scriptlib_


```
import os
import sys
import crossepg
# location of local Python modules under "scripts/lib" and add it to sys.path()
crossepg_instroot = crossepg.epgdb_get_installroot()
if crossepg_instroot == False:
	sys.exit(1)
libdir = os.path.join(crossepg_instroot , 'scripts/lib')
sys.path.append(libdir)

# import scriptlib module
import scriptlib

lg = scriptlib.logging_class()

# write text to stdout and crossepg.log
lg.log("text")
```
During download you can watch in your TV a small window (in lower right corner). You can write text messages into this window.

The window has 2 rows: the upper row is used for the script name showing "Executing script **my\_script\_name\_text**"
```
lg.log2video_scriptname("my_script_name_text")
```
The lower row is used for writing status messages during script execution
```
lg.log2video_status("your_status_text")
```