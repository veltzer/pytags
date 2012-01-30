tagger is a command line tool for tagging files efficiently.
tagger keeps all tags known to it in a central database build
	on top of sqlite and it can search it.
tagger is written in python.
tagger does not rescan files which have been scanned before (unless passed a -force flag)
	for this reason tagger keeps a last modified time in its database.
in the future tagger will scan also for filesystem extended attributes as tags.
	so users will be able to tag binary files too or will be able to tag
	text files without modfying their content.

usage:

tagger scan .
	will scan a folder recursivly and will add its tag information into the database.
tagger search foo
	will list the set of files that have been tagged as foo.
tagger config
	will dump the tagger configuration.
tagger taglist
	will list all tags known to tagger.
tagger clean
	will clear the tagger database.
