#!/bin/sh
CROSS=/opt/dmm/dm800/build/tmp/cross/mipsel/bin/mipsel-oe-linux-
CFLAGS+="-I/opt/dmm/dm800/build/tmp/staging/mipsel-oe-linux/usr/include/libxml2 \
	-I/opt/dmm/dm800/build/tmp/staging/mipsel-oe-linux/usr/include/python2.6" \
CC=${CROSS}gcc \
STRIP=${CROSS}strip \
SWIG=/opt/dmm/dm800/build/tmp/staging/i686-linux/usr/bin/swig \
make
if [ $? != 0 ]; then
	echo compile error
	exit 1
fi

[ -d tmp ] && rm -rf tmp

mkdir -p tmp/CONTROL
mkdir -p tmp/usr/crossepg/aliases
mkdir -p tmp/usr/crossepg/providers
mkdir -p tmp/usr/crossepg/import
mkdir -p tmp/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/skins
mkdir -p tmp/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/images
mkdir -p tmp/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/po/it/LC_MESSAGES

cp bin/* tmp/usr/crossepg/

cp providers/* tmp/usr/crossepg/providers/
cp src/enigma2/python/skins/*.xml tmp/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/skins/
cp src/enigma2/python/images/*.png tmp/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/images/
cp contrib/po/it/LC_MESSAGES/CrossEPG.mo tmp/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/po/it/LC_MESSAGES/
cp contrib/crossepg_epgmove.sh tmp/usr/crossepg/
cp contrib/control tmp/CONTROL/

chmod 755 tmp/usr/crossepg/crossepg_*

# copy with tar so we clean .svn entries
cd contrib
tar --exclude-vcs -zc po | tar -zx -C ../tmp/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/
cd ..

python compileb.py

VERSION=`cat src/version.h | grep RELEASE | sed "s/.*RELEASE \"//" | sed "s/\"//" | sed "s/\ /-/" | sed "s/\ /-/" | sed "s/(//" | sed "s/)//"`
echo "Version: $VERSION-oe1.6" >> tmp/CONTROL/control
echo "Architecture: mipsel" >> tmp/CONTROL/control

sh ipkg-build -o root -g root tmp/

[ ! -d out ] && mkdir out
mv *.ipk out
echo "Package moved in `pwd`/out folder"
