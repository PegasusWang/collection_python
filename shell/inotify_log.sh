#!/bin/bash
inotifywait -mrq --timefmt '%y/%m/%d %H:%M' --format '%T %w%f %e' --event delete,modify,create,attrib /data/web | while read date time file event; do
  case $event in
  MODIFY | CREATE | MOVE | MODIFY,ISDIR | CREATE,ISDIR | MODIFY,ISDIR)
    echo $event'-'$file'-'$date'-'$time >>/var/log/web_watch.log
    ;;

  MOVED_FROM | MOVED_FROM,ISDIR | DELETE | DELETE,ISDIR)
    echo $event'-'$file'-'$date'-'$time /var/log/web_watch.log
    ;;
  esac
done
