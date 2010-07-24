#!/bin/bash
sh ./clean.sh

make -f Makefiles/crossepg_alias.enigma2.mipsel
make -f Makefiles/crossepg_dbconverter.enigma2.mipsel
make -f Makefiles/crossepg_downloader.enigma2.mipsel
make -f Makefiles/crossepg_dbinfo.enigma2.mipsel
make -f Makefiles/crossepg_epgcopy.enigma2.mipsel
make -f Makefiles/crossepg_importer.enigma2.mipsel

python compileb.py

chmod +x enigma2/mipsel/usr/crossepg/crossepg_dbconverter
chmod +x enigma2/mipsel/usr/crossepg/crossepg_dbinfo
chmod +x enigma2/mipsel/usr/crossepg/crossepg_downloader
chmod +x enigma2/mipsel/usr/crossepg/crossepg_epgcopy
chmod +x enigma2/mipsel/usr/crossepg/crossepg_epgmove.sh
chmod +x enigma2/mipsel/usr/crossepg/crossepg_importer

cp src/enigma2/python/*.pyo enigma2/mipsel/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/
mkdir enigma2/mipsel/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/skins
cp src/enigma2/python/skins/*.xml enigma2/mipsel/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/skins

cp -rp po enigma2/mipsel/usr/lib/enigma2/python/Plugins/SystemPlugins/CrossEPG/

# delete apple finder fastidious files
find . | grep "\._" | xargs rm 2>/dev/null
find . | grep "\.DS_Store" | xargs rm 2>/dev/null
find . | grep "\.o$" | xargs rm 2>/dev/null

# get the versione and generate filename
#VERSION=`cat src/common.h | grep RELEASE | sed "s/.*RELEASE \"//" | sed "s/\"//" | sed "s/\ /-/" | sed "s/\ /-/" | sed "s/(//" | sed "s/)//"`
#FILENAME=../crossepg_packages/crossepg-$VERSION-full.tar.gz
#FILENAME_DGS_SH4=../crossepg_packages/crossepg-$VERSION-dgs-sh4.tar.gz
#FILENAME_E1_PPC=../crossepg_packages/crossepg-$VERSION-enigma1-ppc.tar.gz

#tar --exclude-vcs -zcf $FILENAME ../crossepg
#cd dgs
#tar --exclude-vcs -zcf crossepg.tar.gz var
#tar --exclude-vcs -zcf ../$FILENAME_DGS_SH4 crossepg.tar.gz installer.sh
#rm crossepg.tar.gz
#cd ..
#cd enigma1/ppc
#tar --exclude-vcs -zcf ../../$FILENAME_E1_PPC *
#cd ../..

sh ipk.sh

exit 0
