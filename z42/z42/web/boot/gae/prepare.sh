PREFIX=$(cd "$(dirname "$0")"; pwd)


sh $PREFIX/../prepare.sh
python $PREFIX/app_yaml.py 
