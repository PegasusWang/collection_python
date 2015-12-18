PREFIX=$(cd "$(dirname "$0")"; pwd)
BASE=$PREFIX/../../..


#$BASE/z42/web/boot/prepare.sh 

cd $PREFIX
exec python $BASE/z42/web/boot/serve.py $1

