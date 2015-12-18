PREFIX=$(cd "$(dirname "$0")"; pwd)
cd $PREFIX

sh $PREFIX/prepare.sh
ps x -u $USER|ack dev_appserver.py|awk  '{print $1}'|xargs kill -9 > /dev/null 2>&1


DEV=$(python $PREFIX/dev.py $1)
echo ""
echo -e $DEV
echo ""
echo $DEV | sh

