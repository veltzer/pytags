tagger is a command line tool for tagging files efficiently.
tagger keeps all tags known to it in a central database built
	on top of mysql/sqlite and can search it.
tagger is written in python.
tagger does not rescan files which have been scanned before (unless passed a --force flag)
	for this reason tagger keeps a last modified time in its database.
in the future tagger will scan also for filesystem extended attributes as tags.
	so users will be able to tag binary files too or will be able to tag
	text files without modfying their content.

usage:

implemented:
tagger --showconfig
	will dump the tagger configuration.
tagger --testconnect
	Test the connection to the database to see if it's ok.
	This is used to setup tagger correctly or for development purposes.
tagger --create
	will create the database
	If the database exist then tagger will exit.
	If passed --force will remove the old database and create a new one (use with care).
tagger --scan
	will scan the directory 'dir' recursivly (current directory is the default)
	and will add its tag information into the database.
	configuration determines which files are actually scanned (you probably don't want to scan
	some files, like binary files).
	Files which have already been scanned are not scanned.
tagger --search [tags]
	will list the set of files that have been tagged with these tags that are in the requested folder.
	The default for the folder is the current folder.
tagger --taglist
	list all tags known to tagger and their relationships.

future:
tagger --importtags [file]
	import file describing tags and relations between tags.
	tags which are mentioned in this file will have their previous relationships erased.
tagger --clean
	will clean the tagger database.
	must pass --force to show that you really want this.

	Mark Veltzer, 2012
