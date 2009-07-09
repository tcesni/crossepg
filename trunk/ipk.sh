#!/bin/bash

# delete apple finder fastidious files
find . | grep "\._" | xargs rm 2>/dev/null
find . | grep "\.DS_Store" | xargs rm 2>/dev/null
find . | grep "\.o$" | xargs rm 2>/dev/null

VERSION=`cat src/common.h | grep RELEASE | sed "s/.*RELEASE \"//" | sed "s/\"//" | sed "s/\ /-/" | sed "s/\ /-/" | sed "s/(//" | sed "s/)//"`
cat enigma2/sh4/CONTROL/control | sed "s/Version:.*/Version: $VERSION/" > enigma2/sh4/CONTROL/control.tmp
mv enigma2/sh4/CONTROL/control.tmp enigma2/sh4/CONTROL/control
cat enigma2/mipsel/CONTROL/control | sed "s/Version:.*/Version: $VERSION/" > enigma2/mipsel/CONTROL/control.tmp
mv enigma2/mipsel/CONTROL/control.tmp enigma2/mipsel/CONTROL/control
cd enigma2/sh4
tar --exclude-vcs -c * | tar -x -C ../../ipkg-tmp
cd ../..
ipkg-build -o root -g root ipkg-tmp/
rm -rf ipkg-tmp/*
cd enigma2/mipsel
tar --exclude-vcs -c * | tar -x -C ../../ipkg-tmp
cd ../..
ipkg-build -o root -g root ipkg-tmp/
rm -rf ipkg-tmp/*
mv *.ipk ../crossepg_packages