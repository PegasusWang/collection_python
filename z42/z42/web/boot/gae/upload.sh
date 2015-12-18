PREFIX=$(cd "$(dirname "$0")"; pwd)
$PREFIX/z42/boot/init.sh

PREFIX=$PREFIX/../..
echo $PREFIX
cd $PREFIX
deltmp
hg ci -mupload
hg sync

sh $PREFIX/z42/web/boot/gae/prepare.sh
python $PREFIX/z42/web/boot/mako_compile.py
python $PREFIX/z42/web/boot/coffee_script.py -once
python $PREFIX/z42/web/boot/js_requirejs.py release
python $PREFIX/z42/web/boot/coffee_script.py -once
python $PREFIX/z42/web/boot/css_js.py

appcfg.py rollback --oauth2 --noauth_local_webserver $PREFIX
appcfg.py update --oauth2 --noauth_local_webserver $PREFIX


#hg ci -m f
#hg fe 
#hg push
ps x -u $USER|ack 'coffee_script.py'|awk  '{print $1}'|xargs kill -9 > /dev/null 2>&1
