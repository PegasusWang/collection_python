#运行 ./dev.sh -c 就清空数据库

PREFIX=$(cd "$(dirname "$0")"; pwd)

echo $PREFIX

$PREFIX/z42/boot/init.sh

PREFIX=$PREFIX/../..

$PREFIX/z42/web/boot/gae/_dev.sh $1
