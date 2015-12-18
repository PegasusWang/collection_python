
PREFIX=$(cd "$(dirname "$0")"; pwd)
$PREFIX/z42/boot/init.sh

PREFIX=$PREFIX/../..
appcfg.py update_indexes $PREFIX  --oauth2 --noauth_local_webserver 
appcfg.py vacuum_indexes $PREFIX  --oauth2 

