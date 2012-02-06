##########################################################
Tools for XBMC translations and integration with Transifex
##########################################################

``translationtool.py``
######################

``translationtool.py`` is a simple tool to check if XBMC addons ``strings.xml``
files of different languages are in sync.

It parses all the files given as arguments, loops through the files and stores
all IDs it finds, then loops through the IDs and checks if all files have
all the IDs. Any number of files can be compared.

For example, if you have these two language files::

    $ cat English/strings.xml
    <?xml version="1.0" encoding="utf-8" standalone="yes"?>
    <strings>
        <string id="1">Foo</string>
        <string id="2">Bar</string>
    </strings>

    $ cat Backwardslanguage/strings.xml
    <?xml version="1.0" encoding="utf-8" standalone="yes"?>
    <strings>
        <string id="1">Foo</string>
        <string id="3">Baz</string>
    </strings>

Running the tool will give you::

    $ translationtool.py English/strings.xml Backwardslanguage/strings.xml
    Using base: English/strings.xml
    Backwardslanguage/strings.xml
    <string id="2">Bar</string>
    not in base:3

``test-generatexliff.py`` and ``bootstrap.sh``
##############################################

``test-generatexliff.py`` and ``bootstrap.sh`` are for setting up xbmc to use
Transifex.

See also
########

* XBMC Forum thread at http://forum.xbmc.org/showthread.php?t=118978
* Repository for this code:
  https://github.com/viljoviitanen/Simple-XBMC-Translation-Tool/blob/master/bootstrap.sh
* Test project at Transifex: https://www.transifex.net/projects/p/mytest55/
* Test project at Transifex:
  https://www.transifex.net/projects/p/xbmc-main-test/
