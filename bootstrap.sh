#!/bin/bash
#Copyright (C) 2012  Viljo Viitanen <viljo.viitanen@iki.fi>
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#bootstraps languages into transifex from xbmc github
#usage: first parameter: transifex username second parameter: password
#not very pretty code, but I don't care

DIR=/tmp/langs
mkdir -p $DIR

USER=$1
PASS=$2

LANGUAGES="Finnish Hungarian Swedish Afrikaans"

shortcode() {
  case $1 in
  English) SHORT="en" ;;
  Finnish) SHORT="fi" ;;
  Hungarian) SHORT="hu" ;;
  Swedish) SHORT="sv" ;;
  Afrikaans) SHORT="af" ;;
  *) echo "Unknown language $1"; exit 1 ;;
  esac
}


#fetch source xml files from git
for lang in English $LANGUAGES
do
  echo $lang
  [ -f $DIR/confluence.$lang.xml ] || wget https://raw.github.com/xbmc/xbmc/master/addons/skin.confluence/language/$lang/strings.xml -O $DIR/confluence.$lang.xml
  [ -f $DIR/core.$lang.xml ] || wget https://raw.github.com/xbmc/xbmc/master/language/$lang/strings.xml -O $DIR/core.$lang.xml
done

#generate source xliff files
[ -f $DIR/confluence.English.xlf ] || ./test-generatesourcexliff.py $DIR/confluence.English.xml > $DIR/confluence.English.xlf
[ -f $DIR/core.English.xlf ] || ./test-generatesourcexliff.py $DIR/core.English.xml > $DIR/core.English.xlf

#generate xliff files
for lang in $LANGUAGES
do
  echo $lang
  [ -f $DIR/confluence.$lang.xlf ] || ./test-generatexliff.py $DIR/confluence.English.xml $DIR/confluence.$lang.xml > $DIR/confluence.$lang.xlf
  [ -f $DIR/core.$lang.xlf ] || ./test-generatexliff.py $DIR/core.English.xml $DIR/core.$lang.xml > $DIR/core.$lang.xlf
done

[ "x$PASS" = "x" ] && echo "username and password missing" && exit 1

#transifex project slug
PROJECT=mytest55
#transifex resource slugs
CORE=core2
CONFLUENCE=confluence2

#create resources. This is done only once. So uncomment the curl lines below for first run.
#after setup, updating the source language file is different.
#see http://help.transifex.net/features/api/index.html#source-language-methods

#curl -F file=@$DIR/confluence.English.xlf -F name=skin.confluence -F slug=$CONFLUENCE -F i18n_type=XLIFF -i -L --user $USER:$PASS -X POST https://www.transifex.net/api/2/project/$PROJECT/resources/
#curl -F file=@$DIR/core.English.xlf -F name=core -F slug=$CORE -F i18n_type=XLIFF -i -L --user $USER:$PASS -X POST https://www.transifex.net/api/2/project/$PROJECT/resources/

#upload/update translations for resources
for lang in $LANGUAGES
do
  echo $lang
  shortcode $lang
  echo $SHORT
  curl -F file=@$DIR/core.$lang.xlf -i -L --user $USER:$PASS -X PUT https://www.transifex.net/api/2/project/$PROJECT/resource/$CORE/translation/$SHORT/
  curl -F file=@$DIR/confluence.$lang.xlf -i -L --user $USER:$PASS -X PUT https://www.transifex.net/api/2/project/$PROJECT/resource/$CONFLUENCE/translation/$SHORT/
done


