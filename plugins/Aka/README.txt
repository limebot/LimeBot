This plugin allows the user to create various aliases (known as "Akas",
since Alias is the name of another plugin Aka is based on) to other commands
or combinations of other commands (via nested commands).  It is a good
idea to always quote the commands that are being aliased so that any
nested commands are not immediately run.

Basic usage
-----------

Add an aka, trout, which expects a word as an argument

<jamessan> @aka add trout "action slaps $1 with a large trout"
<bot> jamessan: The operation succeeded.
<jamessan> @trout me
* bot slaps me with a large trout

Add an aka, lastfm, which expects a last.fm user and replies with
their recently played items.

@aka add lastfm "rss [format concat http://ws.audioscrobbler.com/1.0/user/ [format concat [urlquote $1] /recenttracks.rss]]"

Note that if the nested commands being aliased hadn't been quoted, then
those commands would have been run immediately, and @lastfm would always
reply with the same information, the result of those commands.
 with any notes, etc. about using it.
