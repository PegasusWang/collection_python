PREFIX=$(cd "$(dirname "$0")"; pwd)
BASE=$PREFIX/../..

while [ 1 ] 
do
$BASE/z42/web/boot/prepare.sh $1
ps x -u $USER|ack $BASE|ack 'z42/web/boot/serve'|awk  '{print $1}'|xargs kill -9 > /dev/null 2>&1
cd $PREFIX
#rm $PREFIX/_html -rf
echo "import _env;import zapp.$(basename $PREFIX).misc.config" > $BASE/z42/_app_config_.py
python $BASE/z42/web/boot/coffee_script.py &
python $BASE/z42/web/boot/serve.py $1

echo ""
for((i=1;i<=4;i++));do echo -n "$i ";sleep 1;done
done
