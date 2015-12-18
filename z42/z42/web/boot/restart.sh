# PREFIX=$(cd "$(dirname "$0")"; pwd) 
# python $PREFIX/cmd/index.py
# BASE=$PREFIX/../../..
# rm -rf $BASE/_html
# $BASE/z42/web/boot/prepare.sh
# python $PREFIX/cmd/restart.py

APPNAME=$1
PREFIX=$(cd "$(dirname "$0")"; pwd) 
BASE=$PREFIX/../../../
APPBASE=$BASE/zapp/$APPNAME

if  [ -z "$APPNAME" ]; then
    echo "You need to specify a app(which locate at zapp) name"
    exit 0
fi

if [ ! -d "$APPBASE" ]; then
    echo "the app "$APPNAME" does not exist"
    exit 0
fi
echo "restarting "$APPNAME"..."
python $PREFIX/index.py $APPNAME
rm -rf $BASE/_html/$APPNAME
$BASE/z42/web/boot/prepare.sh
python $PREFIX/restart.py $APPNAME
