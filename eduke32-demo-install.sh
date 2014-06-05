#!/bin/sh
cat<<E_O_F
# This script will download shareware duke nukem 3d data files
# and after unpacking will show license file which must be accepted
# 
E_O_F

FILES="defs.con duke.rts game.con license.txt user.con duke3d.grp"
MIRROR="ftp://ftp.3drealms.com/share/3dduke13.zip"
TMPFOLDER=$(mktemp -d /tmp/eduke-demo-installer.XXXXXXXXX)
export TMPFOLDER MIRROR FILES

function do_install {
	set -x
	xdg-su -c "cd ${TMPFOLDER}; cp -v ${FILES} /usr/share/games/eduke32/"
	set +x
}
echo ${MSG}
wget -O "${TMPFOLDER}/3dduke13.zip" ${MIRROR}
if [ -s "${TMPFOLDER}/3dduke13.zip" ]; then
	set -x
	unzip -L "${TMPFOLDER}/3dduke13.zip" -d ${TMPFOLDER} dn3dsw13.shr
	unzip -L "${TMPFOLDER}/dn3dsw13.shr" -d ${TMPFOLDER} $FILES
	set +x
else
	echo "File from ${MIRROR} is not accessable check internet connection"
	exit 1
fi
# From here everything should go smoothly (on accept of course)
more "${TMPFOLDER}/license.txt"
echo
echo
echo -n "Do you agree with license terms [y/N]: "
read I_AGREE
case ${I_AGREE} in 
	y|Y|yes|YES|Yes)
		echo "License accepted installing"
		do_install
		;;
	*)
		echo "Sorry license must be agreed upon!"
		exit 1
		;;
esac
set -x
rm -rf ${TMPFOLDER}
exit 0 # normal exit
