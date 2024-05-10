#!/bin/sh

SRC=/var/www/channel/
DST=/var/www/webroot/channel/
INWT=/usr/local/bin/inotifywait
RSYNC=/usr/bin/rsync
$INWT -mrq -e create,move,delete,modify $SRC | while read dir event filename; do
  echo "inotify $dir $event $filename"
  rsync -aHqzt $SRC $DST
done
