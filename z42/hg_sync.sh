hg ci -m "fix" --sub
PREFIX=$(cd "$(dirname "$0")"; pwd)
PREFIX=$(cd "$(dirname "$0")"; pwd)
cd $PREFIX

cd $PREFIX
hg sync

cd $PREFIX/js/_lib 
hg sync

cd $PREFIX/css/_lib 
hg sync
