PREFIX=$(cd "$(dirname "$0")"; pwd)
PREFIX=$PREFIX/../../..
cd $PREFIX

ZWEB=$PREFIX/z42/web



python $ZWEB/boot/env_is_link.py
python $ZWEB/boot/coffee_const.py
python $ZWEB/boot/coffee_script.py -once

python $ZWEB/boot/css_js.py
python $ZWEB/boot/js_requirejs.py
python $ZWEB/boot/signal.py



ps x -u $USER|ack 'coffee_script.py'|xargs kill -9 > /dev/null 2>&1
