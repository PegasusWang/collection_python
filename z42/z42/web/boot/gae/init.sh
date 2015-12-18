PREFIX=$(cd "$(dirname "$0")"; pwd)

APP=`cd \`dirname "$PREFIX/../../.."\`;basename \`pwd\``

PREFIX=$PREFIX
BASE=$PREFIX/../../../..


#cp $PREFIX/app.yaml $BASE
cp_yaml(){
    echo "##########################################" > $BASE/$1
    echo "#DON'T EDIT THIS FILE !!!" >> $BASE/$1
    echo "#EDIT $PREFIX/$1">> $BASE/$1
    echo "#THEN , dev.sh WILL AUTO COPY IT THERE" >> $BASE/$1
    echo "##########################################" >> $BASE/$1
    echo "" >> $BASE/$1
    cat $PREFIX/$1 >> $BASE/$1
}
cp_yaml cron.yaml
cp_yaml index.yaml
cp_yaml backends.yaml 
cp_yaml queue.yaml 

CONFIG="import _env;import zapp.$APP.z42.config" 
echo $CONFIG
echo $CONFIG > $BASE/z42/_app_config_.py

