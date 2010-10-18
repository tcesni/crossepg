OBJS += src/common/memory.o
OBJS += src/common/core/log.o
OBJS += src/common/core/interactive.o
OBJS += src/common/dvb/dvb.o
OBJS += src/common/aliases/aliases.o
OBJS += src/common/net/http.o
OBJS += src/common/opentv/opentv.o
OBJS += src/common/opentv/huffman.o
OBJS += src/common/providers/providers.o
OBJS += src/common/epgdb/epgdb.o
OBJS += src/common/epgdb/epgdb_channels.o
OBJS += src/common/epgdb/epgdb_index.o
OBJS += src/common/epgdb/epgdb_titles.o
OBJS += src/common/epgdb/epgdb_aliases.o
OBJS += src/common/epgdb/epgdb_search.o
OBJS += src/common/xmltv/xmltv_channels.o
OBJS += src/common/xmltv/xmltv_downloader.o
OBJS += src/common/xmltv/xmltv_parser.o
OBJS += src/enigma2/enigma2_hash.o
OBJS += src/enigma2/enigma2_lamedb.o
OBJS += src/common/importer/csv.o
OBJS += src/common/importer/gzip.o
OBJS += src/common/importer/importer.o

CONVERTER_OBJS += src/enigma2/crossepg_dbconverter.o
DBINFO_OBJS += src/common/crossepg_dbinfo.o
DOWNLOADER_OBJS += src/common/crossepg_downloader.o
EPGCOPY_OBJS += src/enigma2/crossepg_epgcopy.o
IMPORTER_OBJS += src/common/crossepg_importer.o
EXPORTER_OBJS += src/common/crossepg_exporter.o
XMLTV_OBJS += src/common/crossepg_xmltv.o

CONVERTER_BIN = bin/crossepg_dbconverter
DBINFO_BIN = bin/crossepg_dbinfo
DOWNLOADER_BIN = bin/crossepg_downloader
EPGCOPY_BIN = bin/crossepg_epgcopy
IMPORTER_BIN = bin/crossepg_importer
EXPORTER_BIN = bin/crossepg_exporter
XMLTV_BIN = bin/crossepg_xmltv

SWIGS_OBJS = src/common/crossepg_wrap.o
SWIGS_LIBS = bin/_crossepg.so

VERSION_HEADER = src/version.h
VERSION_PYTHON = src/enigma2/python/version.py

SVN=$(shell sh get_svn_version.sh)
VERSION=$(shell cat VERSION)

BIN_DIR = bin

FTP_HOST = 172.16.1.139
FTP_USER = root
FTP_PASSWORD = sifteam

all: clean $(CONVERTER_BIN) $(DBINFO_BIN) $(DOWNLOADER_BIN) $(EPGCOPY_BIN) $(IMPORTER_BIN) $(EXPORTER_BIN) $(XMLTV_BIN) $(SWIGS_LIBS)

$(BIN_DIR):
	mkdir -p $@
	
$(VERSION_HEADER):
	echo "#define RELEASE \"$(VERSION) (svn $(SVN))\"" > $(VERSION_HEADER)
	echo "version = \"$(VERSION) (svn $(SVN))\"" > $(VERSION_PYTHON)

$(SWIGS_OBJS):
	$(SWIG) -threads -python $(@:_wrap.o=.i)
	$(CC) $(CFLAGS) -c -fpic -o $@ $(@:.o=.c)
	
$(OBJS): $(VERSION_HEADER) $(BIN_DIR)
	$(CC) $(CFLAGS) -c -fpic -o $@ $(@:.o=.c) -DE2 -DSTANDALONE

$(CONVERTER_OBJS):
	$(CC) $(CFLAGS) -c -o $@ $(@:.o=.c) -DE2 -DSTANDALONE

$(DOWNLOADER_OBJS):
	$(CC) $(CFLAGS) -c -o $@ $(@:.o=.c) -DE2 -DSTANDALONE

$(EPGCOPY_OBJS):
	$(CC) $(CFLAGS) -c -o $@ $(@:.o=.c) -DE2 -DSTANDALONE

$(IMPORTER_OBJS):
	$(CC) $(CFLAGS) -c -o $@ $(@:.o=.c) -DE2 -DSTANDALONE

$(EXPORTER_OBJS):
	$(CC) $(CFLAGS) -c -o $@ $(@:.o=.c) -DE2 -DSTANDALONE

$(XMLTV_OBJS):
	$(CC) $(CFLAGS) -c -o $@ $(@:.o=.c) -DE2 -DSTANDALONE

$(SWIGS_LIBS): $(SWIGS_OBJS)
	$(CC) $(LDFLAGS) -shared -o $@ $(OBJS) $(SWIGS_OBJS) -lxml2 -lz -lm -lpthread
	
$(DBINFO_OBJS):
	$(CC) $(CFLAGS) -c -o $@ $(@:.o=.c) -DE2 -DSTANDALONE

$(CONVERTER_BIN): $(OBJS) $(CONVERTER_OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(CONVERTER_OBJS) -lxml2 -lz -lm -lpthread
	$(STRIP) $@

$(DBINFO_BIN): $(OBJS) $(DBINFO_OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(DBINFO_OBJS) -lxml2 -lz -lm -lpthread
	$(STRIP) $@
	
$(DOWNLOADER_BIN): $(OBJS) $(DOWNLOADER_OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(DOWNLOADER_OBJS) -lxml2 -lz -lm -lpthread
	$(STRIP) $@

$(EPGCOPY_BIN): $(OBJS) $(EPGCOPY_OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(EPGCOPY_OBJS) -lxml2 -lz -lm -lpthread
	$(STRIP) $@

$(IMPORTER_BIN): $(OBJS) $(IMPORTER_OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(IMPORTER_OBJS) -lxml2 -lz -lm -lpthread
	$(STRIP) $@

$(EXPORTER_BIN): $(OBJS) $(EXPORTER_OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(EXPORTER_OBJS) -lxml2 -lz -lm -lpthread
	$(STRIP) $@

$(XMLTV_BIN): $(OBJS) $(XMLTV_OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(XMLTV_OBJS) -lxml2 -lz -lm -lpthread
	$(STRIP) $@
	
clean:
	rm -f $(OBJS) $(CONVERTER_OBJS) $(DOWNLOADER_OBJS) $(EPGCOPY_OBJS) $(IMPORTER_OBJS) \
	$(EXPORTER_OBJS) $(XMLTV_OBJS) $(DBINFO_OBJS) $(CONVERTER_BIN) $(DBINFO_BIN) $(DOWNLOADER_BIN) \
	$(EPGCOPY_BIN) $(IMPORTER_BIN) $(EXPORTER_BIN) $(XMLTV_BIN) $(VERSION_HEADER) \
	$(SWIGS_OBJS) $(SWIGS_LIBS)

install:
	install -d $(D)/usr/crossepg/aliases
	install -d $(D)/usr/crossepg/import
	install -d $(D)/usr/crossepg/providers
	install -d $(D)/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/skins
	install -d $(D)/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/images
	install -d $(D)/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/po/it/LC_MESSAGES
	install -d $(D)/usr/lib/python2.6/lib-dynload
	install -m 755 bin/crossepg_dbconverter $(D)/usr/crossepg/
	install -m 755 bin/crossepg_dbinfo $(D)/usr/crossepg/
	install -m 755 bin/crossepg_downloader $(D)/usr/crossepg/
	install -m 755 bin/crossepg_epgcopy $(D)/usr/crossepg/
	install -m 755 bin/crossepg_importer $(D)/usr/crossepg/
	install -m 755 bin/crossepg_exporter $(D)/usr/crossepg/
	install -m 755 bin/crossepg_xmltv $(D)/usr/crossepg/
	install -m 755 contrib/crossepg_epgmove.sh $(D)/usr/crossepg/
	install -m 644 providers/* $(D)/usr/crossepg/providers/
	install -m 644 contrib/po/it/LC_MESSAGES/CrossEPG.mo $(D)/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/po/it/LC_MESSAGES/
	install -m 644 src/enigma2/python/*.py $(D)/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/
	install -m 644 src/enigma2/python/skins/*.xml $(D)/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/skins/
	install -m 644 src/enigma2/python/images/*.png $(D)/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/images/
	install -m 644 src/common/crossepg.py $(D)/usr/lib/python2.6
	install -m 644 bin/_crossepg.so $(D)/usr/lib/python2.6/lib-dynload

remote-install:
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/lib/python2.6 src/common/crossepg.py
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/lib/python2.6/lib-dynload bin/_crossepg.so

	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/crossepg bin/crossepg_dbconverter
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/crossepg bin/crossepg_dbinfo
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/crossepg bin/crossepg_downloader
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/crossepg bin/crossepg_epgcopy
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/crossepg bin/crossepg_importer
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/crossepg bin/crossepg_exporter
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/crossepg bin/crossepg_xmltv
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/crossepg contrib/crossepg_epgmove.sh

	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/crossepg/providers providers/*
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/po/it/LC_MESSAGES contrib/po/it/LC_MESSAGES/CrossEPG.mo
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG src/enigma2/python/*.py
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/skins src/enigma2/python/skins/*.xml
	ncftpput -m -u $(FTP_USER) -p $(FTP_PASSWORD) $(FTP_HOST) /usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/images src/enigma2/python/images/*.png
	