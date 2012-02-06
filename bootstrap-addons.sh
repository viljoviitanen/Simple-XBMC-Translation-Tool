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
#third parameter:
# if create = create resources with source files
# if update: update source
# if something else (whatever): update only translations
# if missing: error
#not very pretty code, but I don't care
#except the amount of copypastecode is almost frightening

#this needs to be a checked out xbmc git repo! change
A=/home/viljo/git/xbmc/addons

if [ ! -d $A/skin.confluence ]; then
  echo "Change the directory of checked out xbmc git tree in the script!"
  exit 1
fi

DIR=/tmp/langs
mkdir -p $DIR

USER=$1
PASS=$2
THIRD=$3

shortcode() {
  case "$1" in
  Afrikaans) SHORT="af" ;;
  Arabic) SHORT="ar" ;;
  Bulgarian) SHORT="bg" ;;
  Catalan) SHORT="ca" ;;
  Chinese\ \(Simple\)) SHORT="zh" ;;
  Chinese\ \(Traditional\)) SHORT="zh_HK" ;;
  Czech) SHORT="cs" ;;
  Danish) SHORT="da" ;;
  Dutch) SHORT="nl" ;;
  English) SHORT="en" ;;
  Finnish) SHORT="fi" ;;
  French) SHORT="fr" ;;
  German) SHORT="de" ;;
  Greek) SHORT="el" ;;
  Hungarian) SHORT="hu" ;;
  Icelandic) SHORT="is" ;;
  Italian) SHORT="it" ;;
  Japanese) SHORT="ja" ;;
  Korean) SHORT="ko" ;;
  Lithuanian) SHORT="lt" ;;
  Norwegian) SHORT="no" ;;
  Polish) SHORT="pl" ;;
  Portuguese) SHORT="pt" ;;
  Portuguese\ \(Brazil\)) SHORT="pt_BR" ;;
  Romanian) SHORT="ro" ;;
  Russian) SHORT="ru" ;;
  Serbian) SHORT="sr@latin" ;;
  Serbian\ \(Cyrillic\)) SHORT="sr" ;;
  Slovak) SHORT="sk" ;;
  Slovenian) SHORT="sl" ;;
  Spanish) SHORT="es" ;;
  Swedish) SHORT="sv" ;;
  Turkish) SHORT="tr" ;;

  *) echo "Unknown language $1"; exit 1 ;;
  esac
}

#generate source xliff files
for addon in `ls $A|grep confluence`
do

  echo trying $addon
  if [ -d "$A/$addon/language/English" ] 
  then
    B="$A/$addon/language"
  elif [ -d "$A/$addon/resources/language/English" ] 
  then
    B="$A/$addon/resources/language"
  else
    continue
  fi
  [ -f $DIR/$addon.English.xlf ] || ./test-generatesourcexliff.py $B/English/strings.xml  > $DIR/$addon.English.xlf
  ls $B | while read lang
  do
    [ "$lang" = "English" ] && continue
    echo $lang
    shortcode "$lang" || exit 1 
    echo $SHORT
    [ -f $DIR/$addon.$SHORT.xlf ] || ./test-generatexliff.py $B/English/strings.xml  "$B/$lang/strings.xml" > $DIR/$addon.$SHORT.xlf 
  done
done || exit 1

#transifex project slug
PROJECT=mytest55

[ "x$PASS" = "x" ] && echo "username and password missing" && exit 1

if [ "x$THIRD" = "x" ]; then
  echo "third parameter needs to be firstrun (create resources), update (to update source) or something else (to update only translations)"
  exit 1
elif [ "$THIRD" = "firstrun" ]; then

  #create resources
  for addon in `ls $A`
  do
    [ -f "$DIR/$addon.English.xlf" ] || continue
    slug=`echo $addon | sed s/[.]//g`
    curl -f -F file=@$DIR/$addon.English.xlf -F name=$addon -F slug=$slug -F i18n_type=XLIFF -i -L --user $USER:$PASS -X POST https://www.transifex.net/api/2/project/$PROJECT/resource/ || exit 1
  done || exit 1

elif [ "$THIRD" = "update" ]; then
  #update source
  for addon in `ls $A`
  do
    [ -f "$DIR/$addon.English.xlf" ] || continue
    slug=`echo $addon | sed s/[.]//g`
    curl -f -F file=@$DIR/$addon.English.xlf -F name=$addon -F slug=$slug -F i18n_type=XLIFF -i -L --user $USER:$PASS -X PUT https://www.transifex.net/api/2/project/$PROJECT/resource/$slug/content/ || exit 1
  done || exit 1
fi

#upload/update translations for resources
for addon in `ls $A`
do
  [ -f "$DIR/$addon.English.xlf" ] || continue
  slug=`echo $addon | sed s/[.]//g`
  if [ -d "$A/$addon/language/English" ] 
  then
    B="$A/$addon/language"
  elif [ -d "$A/$addon/resources/language/English" ] 
  then
    B="$A/$addon/resources/language"
  else
    continue
  fi
  ls $B | while read lang
  do
    [ "$lang" = "English" ] && continue
    echo $lang
    shortcode "$lang"
    echo $SHORT
    if [ ! -s $DIR/$addon.$SHORT.xlf ]; then
      echo ==== $addon.$SHORT.xlf empty
      exit 1
    fi
    [ -f $DIR/.$addon.$SHORT.xlf ] || curl -f -F file=@$DIR/$addon.$SHORT.xlf -i -L --user $USER:$PASS -X PUT https://www.transifex.net/api/2/project/$PROJECT/resource/$slug/translation/$SHORT/ || exit 1
    touch $DIR/.$addon.$SHORT.xlf
  done || exit 1
done || exit 1

 
